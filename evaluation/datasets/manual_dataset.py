from evaluation.datasets.deepeval_login import run_login
from deepeval.dataset import EvaluationDataset,Golden
import json
from pathlib import Path

run_login()
project_root = Path(__file__).parent.parent.parent
dataset_path = project_root / "data" / "evaluation" / "manual_goldens.json"

with open(dataset_path, "r") as f:
    data = json.load(f)

goldens=[]
for item in data:
    g = Golden(
        input = item["question"],
        expected_output=", ".join(item["key_points"]) 
    )
    goldens.append(g)

dataset = EvaluationDataset(goldens=goldens)
dataset.push(alias = "Manual Golden Dataset")
