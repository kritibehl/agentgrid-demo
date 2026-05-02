import argparse
import json
import os
import statistics
import sys
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.app import run_file

CASES = [
    "data/docs/deployment_failure.txt",
    "data/logs/service_logs.txt",
    "data/runbooks/db_timeout.txt",
    "data/failure_cases/missing_context.txt",
    "data/failure_cases/conflicting_docs.txt",
    "data/failure_cases/tool_failure.txt",
    "data/failure_cases/slow_tool_latency_breach.txt",
    "data/failure_cases/unsupported_answer.txt",
    "data/failure_cases/low_retrieval_hit_rate.txt",
]

def p95(values):
    values = sorted(values)
    if not values:
        return 0
    idx = round((len(values) - 1) * 0.95)
    return values[idx]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=25)
    parser.add_argument("--real", action="store_true")
    args = parser.parse_args()

    os.environ["USE_REAL_MODEL"] = "true" if args.real else "false"

    out_dir = Path("reports/mixed_batch")
    out_dir.mkdir(parents=True, exist_ok=True)

    decisions = Counter()
    reasons = Counter()
    tool_success = []
    latencies = []
    runs = []

    for i in range(args.n):
        case = CASES[i % len(CASES)]
        result = run_file(case)

        decision = result["eval_gate"]["final_decision"]
        reason = result["eval_gate"]["reason"]
        decisions[decision] += 1
        reasons[reason] += 1

        metrics = result["metrics"]
        latency = metrics.get("real_model_latency_ms", metrics.get("local_mock_latency_ms", 0))
        latencies.append(latency)
        tool_success.append(metrics.get("tool_call_success_rate", 0))

        runs.append({
            "run_id": i + 1,
            "case": case,
            "decision": decision,
            "reason": reason,
            "model_mode": result["agent_output"].get("model_mode"),
            "latency_ms": latency,
            "retrieval_hit_rate": metrics.get("retrieval_hit_rate"),
            "tool_call_success_rate": metrics.get("tool_call_success_rate"),
            "estimated_cost_per_request": metrics.get("estimated_cost_per_request"),
        })

    summary = {
        "mode": "real_gemini" if args.real else "mock",
        "total_runs": args.n,
        "decision_counts": dict(decisions),
        "ship_count": decisions.get("ship", 0),
        "hold_count": decisions.get("hold", 0),
        "escalate_count": decisions.get("escalate", 0),
        "top_failure_reason": reasons.most_common(1)[0][0] if reasons else None,
        "reason_counts": dict(reasons),
        "latency_p50_ms": round(statistics.median(latencies), 2) if latencies else 0,
        "latency_p95_ms": round(p95(latencies), 2),
        "tool_call_success_rate_avg": round(sum(tool_success) / len(tool_success), 2) if tool_success else 0,
        "runs": runs,
    }

    output_path = out_dir / ("real_summary.json" if args.real else "mock_summary.json")
    output_path.write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
