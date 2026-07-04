# Architecture & Design

## System Overview

This suite is built around a **single-turn evaluation loop**: for each test query, retrieve relevant context, generate an answer, and measure quality with DeepEval metrics.

```
JPMorgan 10-K PDF
       ↓
   [Ingest & Chunk]
       ↓
   [Embed & Store in Chroma]
       ↓
   [Evaluation Loop]
       ├─ Query
       ├─ Retrieve (top-k similar chunks)
       ├─ Generate (LLM + context)
       ├─ Score (DeepEval metrics)
       └─ Push to Confident AI
```

---

## Component Breakdown

### 1. Ingestion (`app/ingestion/`)

**Purpose**: Load PDF → extract text → split into chunks → prepare for embedding

**Components**:
- **PDF Loader** (`pdf_loader.py`): Uses PyMuPDF (fitz) to extract text and metadata
  - Handles scanned PDFs (OCR via PyMuPDF)
  - Preserves page boundaries and metadata
- **Document Cleaner** (`document_cleaner.py`): Removes noise, normalizes whitespace
  - Strips extra newlines and artifacts from OCR
  - Preserves semantic structure
- **Splitter** (`splitter.py`): LangChain recursive character splitter
  - Configurable chunk size (default: 800 tokens)
  - Configurable overlap (default: 600 tokens)
  - Overlap preserves context across chunk boundaries
- **Chunk Builder**: Adds metadata (page number, chunk index) to each chunk

**Data Flow**:
```
PDF (binary) → PyMuPDF → Raw text (with OCR noise)
→ Clean → Split → [Chunk + metadata]
```

**Key Decision**: Why overlap?
- **With overlap**: Queries near chunk boundaries find relevant context
- **Without overlap**: Risk losing cross-boundary relevance
- **Trade-off**: Storage cost vs. retrieval quality (we chose quality)

---

### 2. Embeddings & Vector Store (`app/retrievers/`)

**Purpose**: Store chunks + embeddings in searchable vector DB

**Components**:
- **Embedding Model**: Nomic Embed Text (via Ollama)
  - Retrieval-optimized embeddings
  - Runs locally (no API cost)
- **Vector Store**: Chroma (SQLite backend)
  - Persisted at `data/vectorstores/chroma_langchain_db/`
  - Fast cosine similarity search
  - Pre-populated for experiments (no re-embedding per run)
- **Retriever Factory** (`retriever_factory.py`): Constructs retrievers
  - **Similarity**: Basic cosine similarity (top-k)
  - **MMR**: Maximal Marginal Relevance (reduce duplicates, but see results below)

**Data Flow**:
```
Chunks → Nomic Embed → Embeddings
→ Chroma (SQLite) → Persisted DB (reused)
```

**Experiment Finding**: For scanned documents, **similarity outperforms MMR**
- MMR reduces duplicate chunks but loses recall on dense documents
- Similarity retrieval: simpler, more effective for finance PDFs

---

### 3. LLM Integration (`app/llms/`)

**Purpose**: Generate answers grounded in retrieved context

**Components**:
- **Chat Model** (`llm_provider.py`): Ollama integration
  - Model: Qwen 2.5 (small, fast, grounded)
  - Runs locally (no API cost or latency)
  - Loaded once and cached
- **Generation Service** (`generation_service.py`): Orchestrates retrieval + generation
  - Retrieves context for query
  - Passes context + query to prompt template
  - Returns generated answer

**Why Qwen 2.5?**
- Small enough to run on CPU/GPU locally
- Instruction-tuned (follows prompt constraints)
- Good faithfulness (low hallucination rate) — see final eval (0.89)

---

### 4. RAG Chain (`app/chains/rag_chain.py`)

**Purpose**: Wire retriever + LLM + prompt + memory into a single runnable

**Design** (using LangChain LCEL):
```python
{
    "retriever_context": retrieve(query),
    "query": query,
    "history": chat_history
}
| prompt_template
| llm
| output_parser
```

**Key Features**:
- **Flexible context**: Can accept pre-computed context (for evaluation) or retrieve on-the-fly
- **Session history**: Attached for multi-turn capability (unused in evaluation, but available)
- **Composable**: Easy to swap retriever, LLM, or prompt

---

### 5. Prompts (`app/prompts/`)

**Purpose**: Format query + context into a structured prompt

**Template**:
```
You are a financial analyst. Answer the question based ONLY on the provided context.

Context:
{retriever_context}

Question: {query}

Answer:
```

**Why this format?**
- **Clear instructions**: "based ONLY on context" reduces hallucination
- **Structured input**: Retriever context is clearly separated
- **Simple**: Avoids unnecessary complexity for evaluation

---

### 6. Session Memory (`app/memory/`)

**Purpose**: Store chat history (optional; not used in evaluation)

**Components**:
- **Session History** (`session_history.py`): In-memory store per session
  - Keyed by session_id
  - Stores user messages + assistant responses
  - Cleared on demand (Streamlit app only)

**Why separate?** Keeps memory logic isolated; evaluation doesn't use memory.

---

## Evaluation Pipelines (`evaluation/`)

### Runner (`evaluation/pipelines/runner.py`)

**Purpose**: Execute final experiment with configured parameters

**Flow**:
1. Load config from `evaluation/configs/final.yaml`
2. Initialize retriever (similarity, top_k=6)
3. Initialize LLM (Ollama Qwen 2.5)
4. Load testcases (from `data/evaluation/manual_goldens.json`)
5. For each testcase:
   - Retrieve top-6 chunks
   - Generate answer
   - Score with DeepEval metrics
6. Push results to Confident AI dashboard

**Output**: Metrics + traces in DeepEval workspace

---

### Testcase Generation (`evaluation/pipelines/generate_testcases.py`)

**Purpose**: Create synthetic Q&A pairs from chunks

**Process**:
1. Sample chunks from vector store
2. For each chunk, prompt LLM: "Generate 1-2 questions this chunk answers"
3. Answers are the chunk content
4. Save as DeepEval testcases

**Result**: ~50-100 synthetic testcases (configurable)

**Trade-off**: Synthetic ≠ real; but gives us baseline metrics and fast iteration

---

### Manual Evaluation (`evaluation/human_eval/run_single_eval.py`)

**Purpose**: Step through individual queries with full tracing

**Flow**:
1. Load manual goldens from `data/evaluation/manual_goldens.json`
2. For each query:
   - Display query
   - Retrieve chunks (show all 6)
   - Generate answer
   - Display metrics
   - Show answer vs. chunk content
3. Optional: Save trace to OpenAI for further analysis

**Use Case**: Debug specific failures, validate metric interpretations

---

### Metrics & Tracing

**DeepEval Metrics**:
- **Answer Relevancy** (0–1): Does the answer match the question?
- **Faithfulness** (0–1): Is the answer grounded in context (no hallucination)?
- **Contextual Precision** (0–1): Are retrieved chunks relevant to the query?
- **Contextual Recall** (0–1): Are all relevant chunks retrieved?
- **Contextual Relevancy** (0–1): Overall retrieval quality

**Traces**: OpenAI tracing captures:
- Query
- Retrieved chunks
- Generated answer
- Metric scores
- Token usage

---

## Configuration (`evaluation/configs/final.yaml`)

**Current config** (`final.yaml`):
```yaml
experiment_name: final_single_turn_evaluation

retriever:
  type: similarity    # "similarity" or "mmr"
  k: 6               # top-k chunks to retrieve

chunking:
  chunk_size: 800     # tokens per chunk
  chunk_overlap: 600  # token overlap between chunks
```

**How to run experiments**:
1. Edit `final.yaml` (e.g., change `k: 4` or `chunk_size: 1024`)
2. Run `python evaluation/pipelines/runner.py`
3. Results push to DeepEval dashboard (compare experiments visually)

**Previous experiments** (archived in reports):
- `topk_exp` (v3): k=4 → 6, improved recall 0.53 → 0.57
- `mmr_exp` (v4): similarity vs. MMR, found similarity better for scanned docs

---

## Data Storage

### Vector Store: `data/vectorstores/chroma_langchain_db/`

**Format**: SQLite (Chroma's default persistence)
- **File**: `data/vectorstores/chroma_langchain_db/chroma.db`
- **Size**: ~37 MB (includes embeddings + metadata)
- **Content**: JPMorgan 10-K chunks + Nomic embeddings
- **Reused**: Same store across all experiments (no re-embedding)

### Raw Documents: `data/raw_docs/`

**File**: `JPmorgan10kReport.pdf`
- **Source**: JPMorgan Chase official 10-K filing (scanned)
- **Size**: ~50 pages
- **Use**: Ingested once, chunks stored in Chroma

### Evaluation Data: `data/evaluation/`

**File**: `manual_goldens.json`
```json
[
  {
    "question": "What is JPMorgan's net income?",
    "expected_answer": "..."  // or manual summary
  },
  ...
]
```

**Use**: Manual evaluation runner reads this file

---

## External Services

### Confident AI (DeepEval)

**Purpose**: Cloud-based evaluation metrics + dashboard
**Required**: `CONFIDENT_API_KEY` in `.env`
**Usage**: 
- Metrics computed locally, results pushed to cloud
- Dashboard shows experiment trends + traces

### OpenAI (Tracing)

**Purpose**: Optional trace logging for debugging
**Required**: `OPENAI_API_KEY` in `.env`
**Usage**:
- Traces captured during evaluation
- Viewable in OpenAI dashboard
- Helps debug metric interpretations

### Ollama (Local)

**Purpose**: LLM + embeddings (no cloud cost)
**Required**: `ollama serve` running locally
**Usage**:
- Qwen 2.5 for generation
- Nomic Embed Text for embeddings
- No API keys needed

---

## Scaling & Customization

### To adapt to other documents:

1. **Replace PDF**:
   - Add your PDF to `data/raw_docs/`
   - Update `ingestion/pdf_loader.py` to point to new file
   - Re-run ingestion → re-embed → run evaluation

2. **Customize chunking**:
   - Edit `evaluation/configs/final.yaml` (chunk_size, overlap)
   - Re-run ingestion
   - Results change only if chunks change

3. **Change LLM**:
   - Update `OLLAMA_MODEL` in `.env` or `app/llms/llm_provider.py`
   - Must be available via `ollama pull model_name`

4. **Change embeddings**:
   - Update `app/retrievers/retriever_factory.py` (embedding model name)
   - Re-embed (clear Chroma DB first)

5. **Extend metrics**:
   - Add custom DeepEval metric classes
   - Wire into `evaluation/pipelines/single_turn_eval.py`

---

## Performance Notes

### Speed
- **Ingestion**: 1–2 min (PDF → chunks → embed)
- **Retrieval**: <100ms per query (Chroma/SQLite)
- **Generation**: 2–5s per query (Qwen 2.5 on CPU)
- **Evaluation**: ~10s per query (DeepEval metrics)

### Memory
- **Vector store**: ~37 MB (SQLite file)
- **LLM**: ~2 GB (Qwen 2.5 loaded in memory)
- **Embeddings**: ~50 MB (Nomic Embed Text)

### Scaling considerations
- For larger docs: Consider async retrieval + batch metric scoring
- For production: Switch to cloud LLM (OpenAI) for lower latency
- For multi-doc: Use Chroma namespaces or separate collections

---

## Troubleshooting

**Ollama connection fails**
- Ensure `ollama serve` is running: `ollama serve` in another terminal
- Check Ollama models: `ollama list`
- Pull missing models: `ollama pull qwen2.5:latest nomic-embed-text`

**DeepEval login fails**
- Verify `CONFIDENT_API_KEY` in `.env`
- Test login: `python -c "from evaluation.datasets.deepeval_login import run_login; run_login()"`

**Low retrieval quality**
- Increase `k` (top_k) in `evaluation/configs/final.yaml`
- Reduce `chunk_overlap` (may be over-duplicating context)
- Check embeddings: are they indexing correctly?

**Slow evaluation**
- Reduce number of testcases
- Batch queries together
- Consider running on GPU (if available)

---

## Next Steps

See [README.md](./README.md) for quick start. See `evaluation/reports/` for detailed experiment analysis.
