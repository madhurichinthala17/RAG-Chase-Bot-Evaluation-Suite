# Baseline Evaluation Summary — baseline_v2

Date:
May 25, 2026

Dataset:
15 manually curated test cases

Changes Introduced:

* Reduced chunk size from 1000 → 800
* Increased chunk overlap from 400 → 600

Metrics Evaluated:

* Answer Relevancy
* Faithfulness
* Contextual Precision
* Contextual Recall
* Contextual Relevancy

Results:

| Metric               | v1   | v2   |
| -------------------- | ---- | ---- |
| Answer Relevancy     | 0.99 | 0.97 |
| Faithfulness         | 0.82 | 0.93 |
| Contextual Precision | 0.67 | 0.73 |
| Contextual Recall    | 0.50 | 0.53 |
| Contextual Relevancy | 0.42 | 0.47 |

Observations:

* Answer generation quality remained consistently strong.
* Retrieval precision and contextual relevancy improved after chunking changes.
* Faithfulness improved significantly, indicating stronger grounding in retrieved context.
* Smaller chunks with higher overlap reduced noisy retrieval and improved semantic coherence.
* Retrieval quality is improving, though contextual recall still indicates missing relevant chunks in some cases.

Key Insight:

The evaluation results suggest that chunking configuration has a major impact on retrieval behavior in scanned-document RAG systems. Improving chunk granularity and overlap increased retrieval quality and grounding consistency without affecting answer relevancy.

Next Planned Experiment:

* Experiment with higher top_k retrieval
* Test MMR retrieval strategy
* Improve OCR preprocessing
* Analyze failed retrieval cases in detail
* Evaluate reranking approaches