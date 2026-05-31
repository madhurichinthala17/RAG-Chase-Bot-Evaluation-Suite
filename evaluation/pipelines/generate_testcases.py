from deepeval.dataset import EvaluationDataset
from deepeval.test_case import LLMTestCase
from evaluation.datasets.deepeval_login import run_login
from evaluation.pipelines._eval_service import get_response_with_context
from app.memory.session_history import clear_session_history

run_login()
dataset = EvaluationDataset()
dataset.pull(alias="Manual Golden Dataset")

test_cases = []
i = 0

def store_testcases(retriever):
    global i
    for golden in dataset.goldens:
        session_id = "abc"
        actual_answer, retrieved_chunks = get_response_with_context(golden.input, session_id, retriever)
        clear_session_history(session_id)
        testcase = LLMTestCase(
            input=golden.input,
            actual_output=actual_answer,
            retrieval_context = [chunk['content'] for chunk in retrieved_chunks],  
            expected_output=golden.expected_output
        )
        test_cases.append(testcase)
        print(f"---- Loaded TC : {i} -----")
        i += 1
    return test_cases

def get_testcases(retriever):
    if len(test_cases) == 0:
        return store_testcases(retriever)
    return test_cases
