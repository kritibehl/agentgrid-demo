from collections import Counter

COUNTERS = Counter()

def record_decision(decision: str, reason: str, tool_success: float):
    COUNTERS["agentgrid_requests_total"] += 1

    if decision == "escalate":
        COUNTERS["agentgrid_escalations_total"] += 1
    elif decision == "hold":
        COUNTERS["agentgrid_hold_total"] += 1
    elif decision == "ship":
        COUNTERS["agentgrid_ship_total"] += 1

    if reason != "passed":
        COUNTERS["agentgrid_validation_failures_total"] += 1

    if tool_success == 0.0:
        COUNTERS["agentgrid_tool_call_failures_total"] += 1

def render_prometheus(latency_p95_ms=258.02, retrieval_hit_rate=0.88):
    lines = [
        "# HELP agentgrid_requests_total Total AgentGrid requests processed",
        "# TYPE agentgrid_requests_total counter",
        f"agentgrid_requests_total {COUNTERS['agentgrid_requests_total']}",
        "# HELP agentgrid_escalations_total Total escalation decisions",
        "# TYPE agentgrid_escalations_total counter",
        f"agentgrid_escalations_total {COUNTERS['agentgrid_escalations_total']}",
        "# HELP agentgrid_hold_total Total hold decisions",
        "# TYPE agentgrid_hold_total counter",
        f"agentgrid_hold_total {COUNTERS['agentgrid_hold_total']}",
        "# HELP agentgrid_ship_total Total ship decisions",
        "# TYPE agentgrid_ship_total counter",
        f"agentgrid_ship_total {COUNTERS['agentgrid_ship_total']}",
        "# HELP agentgrid_validation_failures_total Total validation failures",
        "# TYPE agentgrid_validation_failures_total counter",
        f"agentgrid_validation_failures_total {COUNTERS['agentgrid_validation_failures_total']}",
        "# HELP agentgrid_tool_call_failures_total Total tool-call failures",
        "# TYPE agentgrid_tool_call_failures_total counter",
        f"agentgrid_tool_call_failures_total {COUNTERS['agentgrid_tool_call_failures_total']}",
        "# HELP agentgrid_latency_p95_ms Local evaluation p95 latency in milliseconds",
        "# TYPE agentgrid_latency_p95_ms gauge",
        f"agentgrid_latency_p95_ms {latency_p95_ms}",
        "# HELP agentgrid_retrieval_hit_rate Retrieval hit rate",
        "# TYPE agentgrid_retrieval_hit_rate gauge",
        f"agentgrid_retrieval_hit_rate {retrieval_hit_rate}",
    ]
    return "\n".join(lines) + "\n"
