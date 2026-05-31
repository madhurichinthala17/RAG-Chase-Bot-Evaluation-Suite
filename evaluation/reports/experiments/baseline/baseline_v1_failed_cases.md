# Baseline Evaluation Summary — baseline_v1

Date:
May 25, 2026

Dataset:
15 manually curated test cases

Metrics Evaluated:

* Answer Relevancy
* Faithfulness
* Contextual Precision
* Contextual Recall
* Contextual Relevancy

Results:

| Metric               | Score |
| -------------------- | ----- |
| Answer Relevancy     | 0.99  |
| Faithfulness         | 0.82  |
| Contextual Precision | 0.67  |
| Contextual Recall    | 0.50  |
| Contextual Relevancy | 0.42  |

Observations:

* Answer generation quality is strong.
* Retrieval quality is weaker than generation quality.
* Contextual recall and relevancy are primary bottlenecks.
* System struggles with scanned PDF retrieval consistency.

Next Planned Experiment:

* Reduce chunk size
* Increase chunk overlap
* Improve OCR preprocessing
