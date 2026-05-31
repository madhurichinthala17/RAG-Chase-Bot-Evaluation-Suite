# Final Evaluation Summary — final_v1

Date:
May 30, 2026

Configuration:

- Retriever: Similarity Search
- Top K: 6
- Chunk Size: 800
- Chunk Overlap: 600
- Tracing: DeepEval @observe
- Dataset: 15 Manual Test Cases

Results:

| Metric | Score |
|----------|----------|
| Answer Relevancy | 0.94 |
| Faithfulness | 0.89 |
| Contextual Precision | 0.60 |
| Contextual Recall | 0.50 |
| Contextual Relevancy | 0.55 |

Key Findings:

- Retrieval improvements increased contextual relevancy compared to baseline.
- Faithfulness improved relative to baseline.
- Recall remained largely unchanged.
- OCR quality appears to be a larger bottleneck than chunking strategy.

Conclusion:

Chunking and retrieval tuning improved grounding quality but did not significantly improve retrieval coverage.
![alt text](image.png)