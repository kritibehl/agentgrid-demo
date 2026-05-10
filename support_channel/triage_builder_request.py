import json
import sys
from collections import Counter
from pathlib import Path
from uuid import uuid4


DOC_LINKS = {
    "build_failed": "docs/builder_onboarding.md",
    "publishing_error": "docs/troubleshooting_guide.md",
    "tool_call_failure": "docs/cli_debugging_examples.md",
    "unsupported_answer": "docs/common_failure_modes.md",
    "missing_docs_context": "docs/troubleshooting_guide.md",
    "latency_breach": "docs/common_failure_modes.md",
}


CLI_COMMANDS = {
    "build_failed": "pytest -q && python3 -m src.app --file data/failure_cases/tool_failure.txt",
    "publishing_error": "npm run build && vercel --prod",
    "tool_call_failure": "python3 -m src.support.diagnose --case examples/tool_failure_case.json",
    "unsupported_answer": "python3 -m src.support.diagnose --case examples/unsupported_answer_case.json",
    "missing_docs_context": "python3 -m src.support.diagnose --case examples/retrieval_failure_case.json",
    "latency_breach": "python3 -m src.support.diagnose --case examples/latency_breach_case.json",
}


def classify(message: str) -> str:
    text = message.lower()

    if "build failed" in text:
        return "build_failed"
    if "publishing error" in text or "generated site" in text:
        return "publishing_error"
    if "tool-call" in text or "tool call" in text:
        return "tool_call_failure"
    if "unsupported" in text:
        return "unsupported_answer"
    if "missing docs context" in text or "missing context" in text:
        return "missing_docs_context"
    if "latency" in text or "p95" in text:
        return "latency_breach"

    return "general_support"


def support_response(category: str) -> str:
    responses = {
        "build_failed": "Start with the onboarding validation path, then re-run the local workflow and tests to isolate whether the failure is build-time or validation-time.",
        "publishing_error": "Check the static-site build and deployment path first; confirm the generated artifact includes the expected docs page.",
        "tool_call_failure": "Run the tool-failure diagnosis command and inspect trace_id, tool_call_status, and engineering_bug_summary.",
        "unsupported_answer": "Block the answer, attach the unsupported-output diagnosis, and route to reviewer if evidence is missing.",
        "missing_docs_context": "Confirm the required source/runbook exists, then re-run retrieval diagnosis before approving the response.",
        "latency_breach": "Run latency-breach diagnosis and inspect whether added validation steps increased p95 beyond budget.",
    }
    return responses.get(category, "Collect trace ID, reproduction steps, and affected workflow before routing.")


def engineering_summary(category: str) -> str:
    summaries = {
        "build_failed": "Builder workflow failed before validation completed; inspect build output and validation job status.",
        "publishing_error": "Docs publishing artifact may be stale or missing generated page output.",
        "tool_call_failure": "Retrieval/tool execution failed and returned insufficient evidence for safe response generation.",
        "unsupported_answer": "Generated answer lacked source-backed evidence and should remain blocked until reviewed.",
        "missing_docs_context": "Retriever could not locate required docs/runbook context for the deployment failure.",
        "latency_breach": "Support-validation workflow exceeded latency budget after additional validation step.",
    }
    return summaries.get(category, "General builder support request requires reproduction and trace correlation.")


def triage_requests(requests):
    categories = [classify(item["message"]) for item in requests]
    counts = Counter(categories)

    results = []
    for item, category in zip(requests, categories):
        repeat = counts[category] > 1
        results.append(
            {
                "triage_id": f"triage_{uuid4().hex[:10]}",
                "request_id": item["request_id"],
                "builder": item["builder"],
                "issue_category": category,
                "recommended_doc_link": DOC_LINKS.get(category, "docs/support_faq.md"),
                "cli_command_to_run": CLI_COMMANDS.get(category, "python3 -m src.support.diagnose --case examples/tool_failure_case.json"),
                "support_response_draft": support_response(category),
                "engineering_escalation_summary": engineering_summary(category),
                "repeat_request_flag": repeat,
            }
        )

    return results


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("support_channel/sample_builder_requests.json")
    requests = json.loads(path.read_text())
    results = triage_requests(requests)
    print(json.dumps({"triage_results": results}, indent=2))


if __name__ == "__main__":
    main()
