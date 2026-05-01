from src.rag.retriever import retrieve

def search_docs(query):
    # return full dicts (with source + content + score)
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

    if not findings:
        findings.append("No major issue detected")

    return findings

def create_action_plan(issue):
    if "timeout" in issue.lower():
        return [
            "Check database health and connection pool saturation",
            "Inspect retry behavior and timeout thresholds",
            "Restart or scale the affected dependency if saturation is confirmed",
            "Escalate if latency or error rate remains above threshold",
        ]

    return ["Investigate further and collect additional logs"]
