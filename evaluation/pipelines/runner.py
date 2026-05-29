import yaml
from evaluation.pipelines.single_turn_eval import run
from pathlib import Path

def load_config():
    path_root =Path(__file__).parent.parent
    runner_config_path = path_root/"configs"/"final.yaml"
    with open(runner_config_path, "r") as f:
        return yaml.safe_load(f)
    
def run_single_turn_runner():
    config = load_config()
    run(
        identifier = config["experiment_name"],
        retriever_type = config["retriever"]["type"],
        k = config["retriever"]["k"],
        chunk_size = config["chunking"]["chunk_size"],
        chunk_overlap = config["chunking"]["chunk_overlap"]
    )

if __name__ == "__main__":
    run_single_turn_runner()