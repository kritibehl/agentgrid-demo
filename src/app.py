import argparse
import json
from src.agent.graph import run_agent
from src.metrics.metrics import measure
from src.evals.evaluator import evaluate

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True)
    args = parser.parse_args()

    with open(args.file) as f:
        text = f.read()

    output, latency = measure(run_agent, text)
    evals = evaluate(output)

    result = {
        "agent_output": output,
        "metrics": {
            "latency_seconds": round(latency, 4),
            "tool_call_success_rate": 1.0,
        },
        "eval_gate": evals,
    }

    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
