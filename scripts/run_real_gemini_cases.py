import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.app import run_file

CASES = [
    "data/docs/deployment_failure.txt",
    "data/failure_cases/conflicting_docs.txt",
    "data/failure_cases/unsupported_answer.txt",
]

def main():
    os.environ["USE_REAL_MODEL"] = "true"

    out_dir = Path("reports/real_model_runs")
    out_dir.mkdir(parents=True, exist_ok=True)

    results = []

    for case in CASES:
        result = run_file(case)
        safe_name = Path(case).stem + ".json"
        output_path = out_dir / safe_name
        output_path.write_text(json.dumps(result, indent=2))
        results.append({
            "case": case,
            "output": str(output_path),
            "decision": result["eval_gate"]["final_decision"],
            "reason": result["eval_gate"]["reason"],
            "model_mode": result["agent_output"].get("model_mode"),
        })

    summary = {
        "use_real_model": True,
        "gemini_model": os.getenv("GEMINI_MODEL", "gemini-1.5-flash"),
        "runs": results,
    }

    summary_path = out_dir / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
