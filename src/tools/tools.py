import time
from src.rag.retriever import retrieve

def search_docs(query):
    query_upper = query.upper()

    if "SIMULATE_TOOL_FAILURE" in query_upper or "TOOL_FAILURE" in query_upper:
        raise RuntimeError("simulated document search tool failure")

    if "SIMULATE_SLOW_TOOL" in query_upper or "LATENCY_BREACH" in query_upper:
        time.sleep(0.25)

    return retrieve(query, k=3)

def analyze_logs(log_text):
    text = log_text.lower()
    findings = []

    if "timeout" in text:
        findings.append("Detected timeout issue")

    if "retry" in text:
        findings.append("Detected retry behavior")

    if "latency" in text:
        findings.append("Detected latency degradation")

    if "conflicting" in text or ("doc a" in text and "doc b" in text):
        findings.append("Detected conflicting operational guidance")

    if "delete production data" in text:
        findings.append("Detected unsafe/destructive user request")

    if not findings:
        findings.append("No major issue detected")

    return findings

def create_action_plan(issue):
    if issue == "tool_failure":
        return ["Escalate because required tool execution failed"]

    if issue == "missing_context":
        return ["Hold decision and request missing runbook or dependency context"]

    if issue == "conflicting_docs":
        return ["Escalate to owner because retrieved guidance conflicts"]

    if issue == "latency_breach":
        return ["Hold decision because tool latency exceeded budget"]

    if issue == "unsupported_answer":
        return ["Refuse unsupported/destructive action and request human approval"]

    if issue == "low_retrieval":
        return ["Hold decision because retrieved evidence is insufficient"]

    if "timeout" in issue.lower():
        return [
            "Check database health and connection pool saturation",
            "Inspect retry behavior and timeout thresholds",
            "Restart or scale the affected dependency if saturation is confirmed",
            "Escalate if latency or error rate remains above threshold",
        ]

    return ["Investigate further and collect additional logs"]
