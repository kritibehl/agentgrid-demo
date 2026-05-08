from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel

from src.agent.graph import run_agent
from src.metrics.metrics import measure
from src.metrics.llm_metrics import build_llm_metrics
from src.evals.evaluator import evaluate
from src.tools.autoops_emitter import emit_autoops_event
from src.observability.tracing import new_trace_context
from src.observability.prometheus import record_decision, render_prometheus

app = FastAPI(title="AgentGrid API")

EXPECTED_CONTEXT_COUNT = 3

class AgentRunRequest(BaseModel):
    input: str

@app.get("/health")
def health():
    return {"status": "ok", "service": "agentgrid"}

@app.post("/agent/run")
def agent_run(request: AgentRunRequest):
    output, latency = measure(run_agent, request.input)
    trace_context = new_trace_context(scenario_id=output.get("issue", "unknown"))

    llm_metrics = build_llm_metrics(
        input_text=request.input,
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

    record_decision(evals["final_decision"], evals["reason"], 0.0 if output.get("tool_errors") else 1.0)

    return {
        "agent_output": output,
        "trace": trace_context,
        "metrics": {
            "latency_seconds": round(latency, 4),
            "tool_call_success_rate": 0.0 if output.get("tool_errors") else 1.0,
            **llm_metrics,
        },
        "eval_gate": evals,
        "autoops_event": autoops_event,
    }


@app.get("/metrics", response_class=PlainTextResponse)
def prometheus_metrics():
    return render_prometheus()

@app.post("/run")
def legacy_run(request: AgentRunRequest):
    return agent_run(request)
