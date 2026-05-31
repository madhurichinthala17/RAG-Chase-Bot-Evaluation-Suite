from deepeval import evaluate
from app.retrievers.retriever_factory import build_retriever
from deepeval.tracing import observe
from deepeval.metrics import (
    AnswerRelevancyMetric,
    ContextualPrecisionMetric,
    ContextualRecallMetric,
    ContextualRelevancyMetric,
    FaithfulnessMetric,
)

from evaluation.pipelines.generate_testcases import get_testcases


METRICS = [
    AnswerRelevancyMetric(),
    FaithfulnessMetric(),
    ContextualPrecisionMetric(),
    ContextualRecallMetric(),
    ContextualRelevancyMetric(),
]

def run(identifier,retriever_type,k,chunk_size,chunk_overlap):
    retriever = build_retriever(retriever_type=retriever_type, k=k, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    testcases = get_testcases(retriever)
    evaluate(test_cases=testcases, metrics= METRICS, identifier=identifier)


if __name__ == "__main__":
    run()
