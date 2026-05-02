import argparse
import json
import os
import sys
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.app import run_file

BASE_CASES = [
    "data/docs/deployment_failure.txt",
    "data/logs/service_logs.txt",
    "data/runbooks/db_timeout.txt",
    "data/failure_cases/missing_context.txt",
    "data/failure_cases/conflicting_docs.txt",
    "data/failure_cases/unsupported_answer.txt",
    "data/failure_cases/low_retrieval_hit_rate.txt",
]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=7)
    args = parser.parse_args()

    os.environ["USE_REAL_MODEL"] = "true"

    out_dir = Path("reports/real_model_runs")
    out_dir.mkdir(parents=True, exist_ok=True)

    results = []
    decisions = Counter()
    reasons = Counter()

    for i in range(args.n):
        case = BASE_CASES[i % len(BASE_CASES)]
        result = run_file(case)

        decisions[result["eval_gate"]["final_decision"]] += 1
        reasons[result["eval_gate"]["reason"]] += 1

        output_path = out_dir / f"real_run_{i + 1:02d}_{Path(case).stem}.json"
        output_path.write_text(json.dumps(result, indent=2))

        metrics = result["metrics"]
        results.append({
            "run_id": i + 1,
            "case": case,
            "output": str(output_path),
            "model_mode": result["agent_output"].get("model_mode"),
            "decision": result["eval_gate"]["final_decision"],
            "reason": result["eval_gate"]["reason"],
            "real_model_latency_ms": metrics.get("real_model_latency_ms"),
            "tokens_per_second": metrics.get("tokens_per_second"),
            "estimated_cost_per_request": metrics.get("estimated_cost_per_request"),
            "retrieval_hit_rate": metrics.get("retrieval_hit_rate"),
        })

    summary = {
        "use_real_model": True,
        "gemini_model": os.getenv("GEMINI_MODEL", "gemini-1.5-flash"),
        "total_runs": args.n,
        "decision_counts": dict(decisions),
        "top_failure_reason": reasons.most_common(1)[0][0] if reasons else None,
        "reason_counts": dict(reasons),
        "runs": results,
    }

    summary_path = out_dir / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
