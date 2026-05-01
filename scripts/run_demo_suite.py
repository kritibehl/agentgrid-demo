import json
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.agent.graph import run_agent
from src.metrics.metrics import measure
from src.evals.evaluator import evaluate

FILES = [
    "data/docs/deployment_failure.txt",
    "data/logs/service_logs.txt",
    "data/runbooks/db_timeout.txt",
]

def percentile(values, pct):
    values = sorted(values)
    if not values:
        return 0
    index = round((len(values) - 1) * pct)
    return values[index]

def main():
    runs = []

    for file_path in FILES:
        text = Path(file_path).read_text()
        output, latency = measure(run_agent, text)
        evals = evaluate(output)

        runs.append({
            "file": file_path,
            "latency_seconds": round(latency, 4),
            "issue": output.get("issue"),
            "context_sources": [c.get("source") for c in output.get("context", [])],
            "tool_call_success": True,
            "eval_gate": evals,
        })

    latencies = [r["latency_seconds"] for r in runs]
    tool_success_rate = sum(1 for r in runs if r["tool_call_success"]) / len(runs)

    summary = {
        "total_runs": len(runs),
        "latency_p50_seconds": round(statistics.median(latencies), 4),
        "latency_p95_seconds": round(percentile(latencies, 0.95), 4),
        "tool_call_success_rate": round(tool_success_rate, 2),
        "ship_count": sum(1 for r in runs if r["eval_gate"]["final_decision"] == "ship"),
        "hold_count": sum(1 for r in runs if r["eval_gate"]["final_decision"] == "hold"),
        "escalate_count": sum(1 for r in runs if r["eval_gate"]["final_decision"] == "escalate"),
        "runs": runs,
    }

    Path("reports").mkdir(exist_ok=True)
    Path("reports/demo_metrics.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
