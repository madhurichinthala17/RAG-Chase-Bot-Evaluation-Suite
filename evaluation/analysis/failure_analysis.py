import json
import os
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
results_path = project_root / "evaluation" / "human_eval" / "human_scores.json"
analysis_path  = project_root / "evaluation" / "reports" / "latest" / "v1_failure_analysis.json"

with open(results_path, "r") as f:
    results = json.load(f)

analysed=[]

try:
    for result in results:

        print("\n" + "="*60)
        print(f"ID       : {result['id']}")
        print(f"QUESTION : {result['question']}")
        print(f"\nRETRIEVED CHUNKS:\n")
        content = "".join(chunk['content'] + "\n" for chunk in result['retrieved_chunks'])
        print(content)
        print(f"\nACTUAL ANSWER:\n{result['actual_answer']}")
        print(f"\nSCORES")
        print(f"\nCORRECTNESS: {result['scores']['correctness']}")
        print(f"\nfaithfulness: {result['scores']['faithfulness']}")
        print(f"\nrelevance: {result['scores']['relevance']}")
        error_type = input("Error Type ?")
        reason =input("Reason?")
        print("="*60)
       
        analysed.append({
            "id":               result["id"],
            "question":         result["question"],
            "retrieved_chunks": content,
            "actual_answer":    result["actual_answer"],
            "scores": {
                "correctness":  result['scores']['correctness'],
                "faithfulness": result['scores']['faithfulness'],
                "relevance":    result['scores']['relevance'],
                "error_type": error_type,
                "reason" : reason
            }
        })

        with open(analysis_path, "w") as f:
            json.dump(analysed, f, indent=4)

except KeyboardInterrupt:
    print("\n\nStopped. Run again from begining")
    if os.path.exists(analysis_path):
        os.remove(analysis_path)
