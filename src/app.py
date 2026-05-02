import argparse
import json

from src.agent.graph import run_agent
from src.metrics.metrics import measure
from src.metrics.llm_metrics import build_llm_metrics
from src.evals.evaluator import evaluate
from src.tools.autoops_emitter import emit_autoops_event

EXPECTED_CONTEXT_COUNT = 3

def run_file(file_path: str):
    with open(file_path) as f:
        text = f.read()

    output, latency = measure(run_agent, text)

    llm_metrics = build_llm_metrics(
        input_text=text,
        answer=output.get("answer", ""),
        latency_seconds=latency,
        retrieved_count=len(output.get("context", [])),
        expected_context_count=EXPECTED_CONTEXT_COUNT,
        trace_depth=len(output.get("trace", [])),
    )

    evals = evaluate(output, retrieval_hit_rate=llm_metrics["retrieval_hit_rate"])

    autoops_event = None
    if evals["final_decision"] in ("hold", "escalate"):
        severity = "critical" if evals["final_decision"] == "escalate" else "high"
        autoops_event = emit_autoops_event(
            source="agentgrid",
            issue_type=evals["reason"],
            severity=severity,
            decision=evals["final_decision"],
            reason=evals["reason"],
        )

    mode = output.get("model_mode", "mock")
    latency_key = "real_model_latency_ms" if mode == "gemini" else "local_mock_latency_ms"

    return {
        "agent_output": output,
        "metrics": {
            latency_key: round(latency * 1000, 2),
            "tool_call_success_rate": 0.0 if output.get("tool_errors") else 1.0,
            **llm_metrics,
        },
        "eval_gate": evals,
        "autoops_event": autoops_event,
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True)
    args = parser.parse_args()

    print(json.dumps(run_file(args.file), indent=2))

if __name__ == "__main__":
    main()
