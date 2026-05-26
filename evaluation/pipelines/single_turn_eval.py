from deepeval import evaluate
from deepeval.metrics import (
    AnswerRelevancyMetric,
    ContextualPrecisionMetric,
    ContextualRecallMetric,
    ContextualRelevancyMetric,
    FaithfulnessMetric,
)

from evaluation.pipelines.generate_testcases import get_testcases

IDENTIFIER = "v2"

METRICS = [
    AnswerRelevancyMetric(),
    FaithfulnessMetric(),
    ContextualPrecisionMetric(),
    ContextualRecallMetric(),
    ContextualRelevancyMetric(),
]


def run(identifier: str = IDENTIFIER):
    testcases = get_testcases()
    for metric in METRICS:
        evaluate(test_cases=testcases, metrics=[metric], identifier=identifier)


if __name__ == "__main__":
    run()
