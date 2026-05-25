import json
from pathlib import Path
from evaluation.pipelines._eval_service import get_response_with_context
from app.memory.session_history import clear_session_history

project_root = Path(__file__).parent.parent
dataset_path = project_root / "data" / "evaluation" / "manual_goldens.json"
results_path = project_root / "evaluation" / "reports" / "latest" / "v2_results.json"

def run():
    with open(dataset_path, "r") as f:
        data = json.load(f)

    result_dict = []
    for item in data:
        query = item["question"]
        session_id = "v1dataset"

        actual_answer, retrieved_chunks = get_response_with_context(query, session_id)
        clear_session_history(session_id)

        result_dict.append({
            "id": item["id"],
            "question": query,
            "retrieved_chunks": retrieved_chunks,
            "actual_answer": actual_answer
        })

        print("Done appending " + item["id"])

    with open(results_path, "w") as f:
        json.dump(result_dict, f, indent=4)

if __name__ == "__main__":
    run()
