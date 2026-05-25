# Annotation Guidelines

Purpose: Provide clear instructions for human annotators performing manual review.

Scoring rubric:
- Correctness (1-5): Is the answer factually correct given the retrieved context?
- Faithfulness (1-5): Is the model grounded in the provided chunks (no hallucination)?
- Relevance (1-5): Were the right chunks retrieved for this question?

Notes:
- Annotators must read the retrieved chunks before scoring.
- If unsure, choose the lower score and add a note explaining uncertainty.
- Use the "notes" field to capture edge cases or ambiguous labeling decisions.

Quality control:
- Dual annotation on a 5-10% sample to measure inter-annotator agreement.
- Resolve disagreements via discussion and update guidelines accordingly.
