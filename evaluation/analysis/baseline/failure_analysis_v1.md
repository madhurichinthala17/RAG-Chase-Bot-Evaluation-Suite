Evaluation Results:

Answer Relevancy: 0.99
Faithfulness: 0.82
Contextual Precision: 0.67
Contextual Recall: 0.50
Contextual Relevancy: 0.42

Key Insight:
The chatbot generates relevant and mostly grounded responses, but retrieval quality is weak. The primary bottleneck appears to be retrieval recall and contextual relevancy rather than generation capability.

Likely Causes:

OCR noise from scanned PDFs
fragmented chunking
retrieval of semantically noisy chunks
insufficient overlap between chunks
![alt text](image.png)

Planned Improvements
Reduce chunk size
Increase chunk overlap
Improve OCR preprocessing
Experiment with top_k retrieval
Add retrieval reranking