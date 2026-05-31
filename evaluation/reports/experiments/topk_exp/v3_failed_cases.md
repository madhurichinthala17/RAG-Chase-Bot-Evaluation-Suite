# Retrieval Experiment Summary — v3

Date:
May 25, 2026

Experiment:
Increased retrieval top_k from 4 → 6 after improving chunking configuration.

Metrics Evaluated:

* Answer Relevancy
* Faithfulness
* Contextual Precision
* Contextual Recall
* Contextual Relevancy

Results:

| Metric               | v2   | v3   |
| -------------------- | ---- | ---- |
| Answer Relevancy     | 0.99 | 1.00 |
| Faithfulness         | 0.93 | 0.92 |
| Contextual Precision | 0.73 | 0.73 |
| Contextual Recall    | 0.53 | 0.57 |
| Contextual Relevancy | 0.47 | 0.53 |

Observations:

* Increasing top_k improved contextual recall and contextual relevancy.
* Retrieval coverage improved without significantly reducing precision.
* Faithfulness remained consistently high, indicating grounding quality stayed stable despite broader retrieval.
* Improved chunking configuration likely enabled higher top_k retrieval to become more effective.

Key Insight:

Broader retrieval alone was not sufficient initially, but after improving chunk granularity and overlap, increasing top_k introduced additional useful context without significantly increasing retrieval noise.

Next Planned Experiment:

* Evaluate MMR retrieval strategy
* Improve OCR preprocessing
* Experiment with reranking
* Add observability/tracing