import argparse
import json
from pathlib import Path
from uuid import uuid4


def support_action(issue_type: str) -> str:
    mapping = {
        "tool_failure": "Route incident to engineering owner and inspect tool execution logs.",
        "latency_breach": "Inspect workflow latency and infrastructure bottlenecks.",
        "unsupported_answer": "Block unsafe output and request reviewer approval.",
        "low_retrieval_hit_rate": "Improve retrieval evidence and re-run validation.",
    }
    return mapping.get(issue_type, "Escalate for manual review.")


def engineering_bug(issue_type: str) -> str:
    mapping = {
        "tool_failure": "Support workflow failed because required retrieval/tool execution did not complete.",
        "latency_breach": "Workflow exceeded acceptable validation latency thresholds.",
        "unsupported_answer": "Generated output lacked sufficient evidence support.",
        "low_retrieval_hit_rate": "Retrieval system returned insufficient evidence coverage.",
    }
    return mapping.get(issue_type, "Unknown support-validation failure.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", required=True)
    args = parser.parse_args()

    data = json.loads(Path(args.case).read_text())

    output = {
        "trace_id": f"trace_{uuid4().hex[:16]}",
        "issue_type": data.get("issue_type"),
        "retrieval_hit_rate": data.get("retrieval_hit_rate"),
        "tool_call_status": data.get("tool_call_status"),
        "decision": data.get("decision"),
        "recommended_support_action": support_action(data.get("issue_type")),
        "engineering_bug_summary": engineering_bug(data.get("issue_type")),
    }

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
