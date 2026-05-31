import json
from pathlib import Path

project_root = Path(__file__).parent.parent
results_path = project_root / "evaluation" / "reports" / "latest" / "v1_results.json"
scored_path  = project_root / "evaluation" / "human_eval" / "human_scores.json"

with open(results_path, "r") as f:
    results = json.load(f)

scored = []

def ask_score(label, lo=1, hi=5):
    while True:
        val = input(f"  {label} ({lo}-{hi}): ").strip()
        if val.isdigit() and lo <= int(val) <= hi:
            return int(val)
        print(f"  Please enter a number between {lo} and {hi}.")

try:
    for result in results:

        print("\n" + "="*60)
        print(f"ID       : {result['id']}")
        print(f"QUESTION : {result['question']}")
        print(f"\nRETRIEVED CHUNKS:\n")
        for i in result['retrieved_chunks']:
            print(i['content']+"\n")
        print(f"\nACTUAL ANSWER:\n{result['actual_answer']}")
        print("="*60)

        print("\nScore the following (1=poor, 5=excellent):")
        correctness  = ask_score("Correctness  (is the answer right?)")
        faithfulness = ask_score("Faithfulness (grounded in chunks, no hallucination?)")
        relevance    = ask_score("Relevance    (were the right chunks retrieved?)")
        notes        = input("  Notes (optional, press Enter to skip): ").strip()

        scored.append({
            "id":               result["id"],
            "question":         result["question"],
            "retrieved_chunks": result["retrieved_chunks"],
            "actual_answer":    result["actual_answer"],
            "scores": {
                "correctness":  correctness,
                "faithfulness": faithfulness,
                "relevance":    relevance,
                "notes":        notes
            }
        })

        with open(scored_path, "w") as f:
            json.dump(scored, f, indent=4)

        print(f"✓ Saved ({len(scored)}/{len(results)} done)")

except KeyboardInterrupt:
    print("\n\nStopped. Progress saved — run again to resume.")
