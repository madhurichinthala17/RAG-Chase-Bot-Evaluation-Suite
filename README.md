# RAG Chase-bot Evaluation Suite

> **How different retrieval strategies affect RAG answer quality.** Quantified metrics (Answer Relevancy 0.94, Faithfulness 0.89) from evaluating a production RAG pipeline on scanned financial documents.

![Architecture](assets/architecture.svg)

## Why This Matters

Building RAG systems is easy. Building *good* RAG systems is hard. Most teams don't measure *what* breaks: Is it retrieval? Chunking? Embeddings? This suite answers that question with rigorous metrics and reproducible experiments on real scanned PDFs.

**This is not a demo chatbot.** It's an evaluation framework that shows exactly which decisions impact answer quality.

## Who Should Use This

- **RAG engineers** debugging low retrieval quality or hallucination in production pipelines
- **Finance AI teams** building document-grounded systems on 10-Ks, annual reports, and SEC filings
- **Evaluation practitioners** who need templates for setting up DeepEval metrics on real PDF data
- **Teams scaling from toy datasets to real-world scanned documents**

---

## Key Results

### Final Evaluation (`final_v1`)

| Metric | Score | Notes |
|--------|-------|-------|
| **Answer Relevancy** | 0.94 | Questions matched generated answers effectively |
| **Faithfulness** | 0.89 | Answers grounded in retrieved context |
| **Contextual Precision** | 0.60 | Retrieved chunks were mostly relevant; some noise |
| **Contextual Recall** | 0.50 | Incomplete coverage; OCR/layout noise impact |
| **Contextual Relevancy** | 0.55 | Overall retrieval quality moderate |

### What Changed Our Results

**Retrieval tuning** (`topk_exp` v3): Increased `top_k` from 4 → 6
- Recall improved: 0.53 → 0.57 (+7%)
- Relevancy improved: 0.47 → 0.53 (+13%)
- Precision held steady ✓

**MMR vs. Similarity** (`mmr_exp` v4): MMR reduced duplicate context but hurt recall
- Finding: For scanned documents, simple similarity search > MMR
- Takeaway: Your retrieval strategy depends on your data

---

## What's Inside

```
.
├── app/                          # RAG pipeline components
│   ├── chains/                   # RAG chain construction (LangChain)
│   ├── ingestion/                # PDF loading, cleaning, chunking
│   ├── llms/                     # Ollama integration + inference
│   ├── memory/                   # Session history (chat memory)
│   ├── prompts/                  # Prompt templates + formatting
│   └── retrievers/               # Chroma vector store + retriever factory
├── evaluation/                   # Core evaluation pipelines
│   ├── configs/                  # Experiment config (final.yaml)
│   ├── datasets/                 # DeepEval testcase generation
│   ├── human_eval/               # Manual evaluation runner
│   ├── pipelines/                # Single-turn evaluation driver
│   └── reports/                  # Experiment summaries, analysis, traces
├── data/
│   ├── evaluation/               # Golden testcases (manual_goldens.json)
│   ├── raw_docs/                 # JPMorgan 10-K PDF
│   └── vectorstores/             # Persisted Chroma DB (SQLite-backed)
├── assets/                       # Architecture and flow diagrams
├── streamlit_app.py              # Optional manual inspection UI
├── requirements.txt              # Dependencies
└── README.md
```

### How It Fits Together

1. **Ingestion**: Load JPMorgan 10-K PDF → split into chunks (800 tokens, 600 overlap) → embed with `nomic-embed-text`
2. **Storage**: Persist embeddings in Chroma (SQLite backend, in `data/vectorstores/`)
3. **Retrieval**: For each test query, retrieve top-6 similar chunks
4. **Generation**: Pass chunks + query to Ollama (`qwen2.5:latest`) via LangChain
5. **Evaluation**: Score answers with DeepEval metrics (Relevancy, Faithfulness, Precision, Recall)
6. **Tracing**: Push metrics to DeepEval (Confident AI) for analysis and dashboards

**Key insight**: The pipeline is instrumented end-to-end. Every decision (chunk size, retriever type, embedding model, LLM) is configurable and measurable.

---

## Quick Start

### Prerequisites

- **Python:** 3.11+ (3.12 recommended)
- **Services:** Ollama running locally (`ollama serve`)
- **API Keys:** Confident AI (DeepEval), OpenAI (tracing)

### Setup

1. **Clone and install:**
   ```bash
   git clone https://github.com/madhurichinthala17/RAG-Chase-Bot-Evaluation-Suite.git
   cd RAG-Chase-Bot-Evaluation-Suite
   pip install -r requirements.txt
   ```

2. **Configure secrets:**
   ```bash
   cp .env.example .env
   ```
   Fill in:
   ```ini
   CONFIDENT_API_KEY=your_confident_api_key
   OPENAI_API_KEY=your_openai_api_key
   CONFIDENT_TRACE_FLUSH=1
   ```

3. **Verify Confident AI login:**
   ```bash
   python -c "from evaluation.datasets.deepeval_login import run_login; run_login()"
   ```

### Run the Evaluation

**Execute the final experiment:**
```bash
python evaluation/pipelines/runner.py
```

This runs the configuration in `evaluation/configs/final.yaml` (similarity retrieval, top_k=6, chunk size 800, overlap 600) and writes metrics to DeepEval.

**Run manual evaluation** (step through individual queries):
```bash
python evaluation/human_eval/run_single_eval.py
```

This evaluates curated queries from `data/evaluation/manual_goldens.json`, showing retrieved chunks and generated answers.

**Try the Streamlit app** (optional UI for manual inspection):
```bash
streamlit run streamlit_app.py
```

Then visit `http://localhost:8501` and ask questions about the JPMorgan 10-K.

---

## Behind the Scenes: How It Works

**The experiment runner** (`evaluation/pipelines/runner.py`):
- Loads config from `evaluation/configs/final.yaml`
- Instantiates retriever (similarity, top_k=6) and LLM (Ollama)
- Iterates through testcases (generated or manual)
- For each query: retrieves context → generates answer → scores with DeepEval metrics
- Pushes results to DeepEval dashboard

**Testcase generation** (`evaluation/pipelines/generate_testcases.py`):
- Extracts chunks from the vector store
- Generates synthetic Q&A pairs using an LLM
- Saves as DeepEval testcases

**Vector store** (`data/vectorstores/chroma_langchain_db/`):
- SQLite-backed Chroma DB
- Pre-populated with JPMorgan 10-K embeddings
- Reused across experiments (fast iteration)

**Metrics**:
- **Answer Relevancy**: Does the generated answer match the question?
- **Faithfulness**: Is the answer grounded in the retrieved context (no hallucination)?
- **Contextual Precision**: Are retrieved chunks relevant to the query?
- **Contextual Recall**: Are all relevant chunks retrieved?

---

## Interpretation & Insights

### Why Recall (0.50) Stayed Low

Even with tuning, recall remained challenged (~50%). Root causes:
- **OCR noise**: Scanned PDFs introduce artifacts; embeddings struggle with noisy text
- **Layout complexity**: Financial tables, multi-column layouts don't chunk cleanly
- **Dense information**: A single chunk often contains unrelated facts; hard to retrieve specific points

**Lesson**: For scanned documents, consider:
- Better OCR preprocessing (not just `pymupdf`)
- Hierarchical chunking (table-aware splitting)
- Hybrid retrieval (BM25 + semantic search)

### Why Faithfulness (0.89) Was High

The LLM (Qwen 2.5) stayed grounded even with imperfect retrieval. This suggests:
- The prompt template effectively constrains the LLM to the context
- Qwen 2.5 is conservative (doesn't hallucinate easily)

---

## Stack

- **Language:** Python 3.11+
- **Framework:** LangChain (RAG orchestration) + LangChain-Chroma (vector store) + LangChain-Ollama (LLM)
- **Vector DB:** Chroma (SQLite backend)
- **Embeddings:** Nomic Embed Text (via Ollama)
- **LLM:** Ollama (local inference, Qwen 2.5)
- **Evaluation:** DeepEval (Confident AI) + OpenAI tracing
- **UI:** Streamlit (optional inspection)
- **PDF Loading:** PyMuPDF (fitz)

---

## Comparison with Similar Projects

| Project | Focus | Scope | License |
|---------|-------|-------|---------|
| **RAG Chase-bot Suite** | Evaluation-first; real scanned PDFs | Finance docs; end-to-end pipeline + metrics | MIT |
| [LlamaIndex Evaluation](https://docs.llamaindex.ai/en/stable/module_guides/evaluating/) | General evaluation framework | Flexible; many metrics, less domain-specific | MIT |
| [RAGAS](https://docs.ragas.io/) | RAG evaluation metrics | Framework + metrics; no pipeline included | Apache 2.0 |
| [DeepEval Docs](https://docs.confident-ai.com/) | Evaluation platform | SaaS + open-source; no pipeline template | Proprietary |

**Why choose this suite?**
- ✅ Complete end-to-end pipeline (not just metrics)
- ✅ Specific to scanned documents and finance
- ✅ Reproducible experiments with configuration
- ✅ Real results on real data (not toy examples)

---

## Development Notes

- **Source PDF:** `data/raw_docs/JPmorgan10kReport.pdf` (scanned; OCR via PyMuPDF)
- **Vector store:** `data/vectorstores/chroma_langchain_db/` (persisted; ~37 MB)
- **Chat model:** Qwen 2.5 (via Ollama)
- **Embeddings:** Nomic Embed Text (via Ollama)
- **Core philosophy:** Evaluation quality > conversational UX. The Streamlit app is a bonus, not the focus.

---

## Future Improvements

- [ ] **Hybrid retrieval**: BM25 + semantic search for scanned documents
- [ ] **Table-aware chunking**: Special handling for financial tables
- [ ] **OCR preprocessing**: Noise reduction before embedding
- [ ] **Multi-turn evaluation**: Extend beyond single-turn Q&A
- [ ] **Other domains**: Adapt to medical, legal, or technical documents
- [ ] **Streaming results**: Real-time metric updates during evaluation

---

## License

This project is provided as-is for research and evaluation purposes.

---

## Questions?

- 📖 Check the `evaluation/reports/` directory for detailed experiment notes and traces
- 🔧 See `evaluation/configs/final.yaml` to customize retrieval strategy, chunk size, and overlap
- 🧪 Modify `data/evaluation/manual_goldens.json` to evaluate on your own queries

**Ready to measure your RAG?** Clone, configure, and run. Results go straight to your DeepEval dashboard.
