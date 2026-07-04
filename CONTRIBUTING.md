# Contributing & Adapting This Suite

Thank you for interest in this evaluation framework! This guide explains how to extend, adapt, and contribute improvements.

---

## Getting Started

1. **Fork the repo** on GitHub
2. **Clone your fork**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/RAG-Chase-Bot-Evaluation-Suite.git
   cd RAG-Chase-Bot-Evaluation-Suite
   ```
3. **Set up environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # or `venv\Scripts\activate` on Windows
   pip install -r requirements.txt
   ```
4. **Configure `.env`** (see README)
5. **Verify setup**: Run `python evaluation/pipelines/runner.py` — should complete without errors

---

## Common Contributions

### 1. Add a New Retrieval Strategy

**Goal**: Compare a different retriever (e.g., BM25, Hybrid, LlamaIndex)

**Steps**:
1. Create new retriever in `app/retrievers/retrievers.py`:
   ```python
   class BM25Retriever:
       def __init__(self, docs):
           self.bm25 = BM25(docs)
       
       def invoke(self, query):
           return self.bm25.get_top_k(query, k=6)
   ```

2. Register in `retriever_factory.py`:
   ```python
   def build_retriever(retriever_type, k):
       if retriever_type == "bm25":
           return BM25Retriever(docs)
   ```

3. Add to config `evaluation/configs/experiment_bm25.yaml`:
   ```yaml
   experiment_name: bm25_experiment
   retriever:
     type: bm25
     k: 6
   ```

4. Run: `python evaluation/pipelines/runner.py` (with modified config path)

5. Compare results in DeepEval dashboard

---

### 2. Evaluate on a Different Document

**Goal**: Apply the suite to your own PDFs (e.g., SEC filings, medical docs, legal contracts)

**Steps**:
1. **Add your PDF** to `data/raw_docs/`:
   ```bash
   cp ~/Downloads/your_document.pdf data/raw_docs/
   ```

2. **Update ingestion** in `app/ingestion/pdf_loader.py`:
   ```python
   PDF_PATH = "data/raw_docs/your_document.pdf"  # Change this line
   ```

3. **Re-embed**:
   - Delete old vector store: `rm -rf data/vectorstores/chroma_langchain_db/`
   - Run ingestion: `python app/ingestion/pdf_loader.py` (or embed step in runner)

4. **Create goldens** in `data/evaluation/manual_goldens.json`:
   ```json
   [
     {
       "question": "What is the total revenue?",
       "expected_answer": "Found in section 2, page 5"
     }
   ]
   ```

5. **Run evaluation**: `python evaluation/pipelines/runner.py`

6. **Analyze results**: Check metrics and compare to JPMorgan baseline

---

### 3. Add a Custom Metric

**Goal**: Measure something DeepEval doesn't (e.g., "Is the answer concise?")

**Steps**:
1. Create custom metric in `evaluation/pipelines/custom_metrics.py`:
   ```python
   from deepeval.metrics import BaseMetric
   
   class ConcisennessMetric(BaseMetric):
       def __init__(self):
           self.threshold = 100  # max words
       
       def measure(self, test_case):
           answer_words = len(test_case.actual_output.split())
           score = 1.0 if answer_words <= self.threshold else 0.5
           self.score = score
           return score
   ```

2. Wire into runner in `evaluation/pipelines/single_turn_eval.py`:
   ```python
   from evaluation.pipelines.custom_metrics import ConcisennessMetric
   
   test_case.add_metric(ConcisennessMetric())
   ```

3. Run evaluation → new metric appears in DeepEval dashboard

---

### 4. Improve Chunking Strategy

**Goal**: Test hierarchical, table-aware, or semantic chunking

**Steps**:
1. Create new splitter in `app/ingestion/splitter.py`:
   ```python
   class TableAwareSplitter:
       def split_documents(self, docs):
           # Detect tables, preserve them as single chunks
           # Return split documents
           pass
   ```

2. Update `ingestion/pdf_loader.py` to use new splitter

3. Add config `evaluation/configs/table_aware.yaml`:
   ```yaml
   experiment_name: table_aware_chunking
   chunking:
     strategy: table_aware
   ```

4. Re-embed and evaluate

5. Compare metrics (recall should improve for table-heavy docs)

---

### 5. Multi-Turn Evaluation

**Goal**: Extend from single-turn Q&A to multi-turn conversations

**Steps**:
1. Update testcase format in `data/evaluation/multi_turn_goldens.json`:
   ```json
   [
     {
       "conversation": [
         {"role": "user", "content": "What is JPMorgan's revenue?"},
         {"role": "assistant", "content": "..."},
         {"role": "user", "content": "And expenses?"},
         {"role": "assistant", "content": "..."}
       ],
       "expected": "..."
     }
   ]
   ```

2. Create `evaluation/pipelines/multi_turn_eval.py` (similar to `single_turn_eval.py`)

3. Wire session history into chain (already available in `app/chains/rag_chain.py`)

4. Run evaluation with multi-turn testcases

---

## Code Style & Standards

### Python

- **Format**: Use `black` (or `autopep8`)
  ```bash
  black app/ evaluation/
  ```
- **Linting**: Run `pylint` or `flake8`
  ```bash
  pylint app/
  ```
- **Type hints**: Preferred (optional but helpful)
  ```python
  def retrieve(query: str, k: int = 6) -> list[Document]:
      pass
  ```

### Commits

- **Message format**: `[area] Brief description`
  ```
  [retriever] Add BM25 support
  [metrics] Add conciseness scoring
  [docs] Update architecture guide
  ```
- **Keep commits focused** (one feature per commit)

### Pull Requests

- **Title**: Concise, clear (e.g., "Add hybrid retrieval support")
- **Description**: Explain the problem, your solution, and results
  ```markdown
  ## Problem
  Current retrieval relies only on semantic similarity, missing keyword matches.
  
  ## Solution
  Added BM25 retriever + hybrid scoring (weighted blend).
  
  ## Results
  Recall improved 0.50 → 0.58 on test set.
  ```
- **Testing**: Include sample metrics/comparisons if applicable

---

## Testing

### Manual Testing

1. **Run the suite** on test data:
   ```bash
   python evaluation/pipelines/runner.py
   ```

2. **Check outputs**:
   - Metrics printed to console
   - Results in DeepEval dashboard
   - No errors or crashes

3. **Compare to baseline**:
   - Note baseline metrics (final_v1 results above)
   - Verify your change improves or doesn't degrade them

### Automated Testing (Optional)

Create `tests/test_retriever.py`:
```python
import unittest
from app.retrievers.retriever_factory import build_retriever

class TestRetriever(unittest.TestCase):
    def setUp(self):
        self.retriever = build_retriever("similarity", k=6)
    
    def test_retrieve_returns_list(self):
        results = self.retriever.invoke("test query")
        self.assertIsInstance(results, list)
    
    def test_retrieve_returns_k_results(self):
        results = self.retriever.invoke("test query")
        self.assertEqual(len(results), 6)

if __name__ == "__main__":
    unittest.main()
```

Run:
```bash
python -m pytest tests/
```

---

## Reporting Issues

Found a bug or have a question? Open a GitHub issue with:

1. **Title**: Clear, specific
   - ❌ "It doesn't work"
   - ✅ "Ollama connection fails when running runner.py"

2. **Description**:
   - What you expected
   - What actually happened
   - Steps to reproduce

3. **Environment**:
   ```
   Python: 3.11
   OS: macOS 14.1
   Ollama: 0.1.33
   ```

4. **Stack trace** (if error):
   ```
   Traceback (most recent call last):
     File "evaluation/pipelines/runner.py", line 22, in <module>
       ...
   ```

---

## Ideas for Extension

### Immediate (1-2 hours)
- [ ] Add `Anthropic Claude` or `Cohere` as LLM option
- [ ] Create `evaluation/scripts/batch_eval.py` to run multiple configs
- [ ] Add experiment comparison notebook (`notebooks/compare_results.ipynb`)

### Medium (1-2 days)
- [ ] Implement OCR preprocessing (noise reduction before embedding)
- [ ] Add table detection + table-aware chunking
- [ ] Build CI/CD workflow (GitHub Actions) to run evals on pushes

### Ambitious (1-2 weeks)
- [ ] Extend to multi-turn conversations
- [ ] Add cost/latency tracking (not just quality)
- [ ] Support Llama 2, Mistral, other open LLMs
- [ ] Build web dashboard (alternative to DeepEval)

---

## Code of Conduct

- Be respectful and inclusive
- Assume good faith in discussions
- Focus on the work, not the person

---

## Questions?

- **Check existing issues** before asking
- **Read ARCHITECTURE.md** for deep dives
- **Run manual evaluation** (`evaluation/human_eval/run_single_eval.py`) for debugging

**Thank you for contributing!** Your ideas make this suite better. 🙌
