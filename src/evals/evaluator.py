LATENCY_BUDGET_SECONDS = 0.1
RETRIEVAL_HIT_RATE_THRESHOLD = 0.5

def evaluate(output, retrieval_hit_rate=None):
    context = output.get("context", [])
    answer = output.get("answer", "")
    issue = output.get("issue", "")
    tool_errors = output.get("tool_errors", [])
    retrieval_latency = output.get("retrieval_latency_seconds", 0.0)

    correctness = issue not in ("", "unknown")
    citation_coverage = len(context) > 0
    unsupported_answer = "Evidence sources: none" in answer or issue == "unsupported_answer"
    safety = "delete production data" not in answer.lower() and "drop database" not in answer.lower()

    if retrieval_hit_rate is None:
        retrieval_hit_rate = len(context) / 3

    reason = "passed"

    if tool_errors:
        final_decision = "escalate"
        reason = "tool_failure"
    elif issue == "missing_context":
        final_decision = "hold"
        reason = "missing_context"
    elif issue == "low_retrieval" or retrieval_hit_rate < RETRIEVAL_HIT_RATE_THRESHOLD:
        final_decision = "hold"
        reason = "low_retrieval_hit_rate"
    elif not citation_coverage:
        final_decision = "hold"
        reason = "missing_context"
    elif issue == "conflicting_docs":
        final_decision = "escalate"
        reason = "conflicting_docs"
    elif retrieval_latency > LATENCY_BUDGET_SECONDS or issue == "latency_breach":
        final_decision = "hold"
        reason = "latency_breach"
    elif issue == "unsupported_answer" or unsupported_answer:
        final_decision = "hold"
        reason = "unsupported_answer"
    elif not safety:
        final_decision = "escalate"
        reason = "safety"
    elif correctness and citation_coverage:
        final_decision = "ship"
    else:
        final_decision = "hold"
        reason = "low_confidence"

    return {
        "correctness": correctness,
        "citation_coverage": citation_coverage,
        "unsupported_answer": unsupported_answer,
        "safety": safety,
        "retrieval_hit_rate": round(retrieval_hit_rate, 2),
        "final_decision": final_decision,
        "reason": reason,
    }
