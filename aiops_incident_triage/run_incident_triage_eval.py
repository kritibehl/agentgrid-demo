import json
from pathlib import Path


def has_any(text, terms):
    lower = text.lower()
    return any(term.lower() in lower for term in terms)


def generate_summary(scenario):
    logs = scenario.get("logs", [])
    telemetry = scenario.get("telemetry", {})
    runbooks = scenario.get("runbook_context", [])

    evidence = logs + runbooks
    evidence_text = " ".join(evidence).lower()

    if not runbooks:
        hypothesis = "Evidence is limited; probable cause is unknown pending runbook context and additional traces."
        missing = ["runbook context", "trace_id", "dependency ownership"]
        actions = ["request missing runbook", "collect trace_id", "escalate for manual review"]
    elif "timeout" in evidence_text or "connection pool" in evidence_text:
        hypothesis = "Probable-cause hypothesis: database timeout or connection-pool saturation may be causing retry amplification."
        missing = ["database health snapshot", "connection pool metrics"]
        actions = ["check database health", "inspect connection pool saturation", "reduce retry fanout", "escalate if latency remains above threshold"]
    elif "queue" in evidence_text or "validation" in evidence_text:
        hypothesis = "Probable-cause hypothesis: worker queue pressure or recent validation-step changes may be increasing p95 latency."
        missing = ["worker utilization", "recent validation-step diff"]
        actions = ["inspect queue depth", "check worker saturation", "review recent validation changes"]
    else:
        hypothesis = "Probable-cause hypothesis: incident requires additional evidence before assigning root cause."
        missing = ["additional logs", "trace_id"]
        actions = ["collect logs", "escalate for manual review"]

    return {
        "scenario_id": scenario["scenario_id"],
        "incident_summary": f"{scenario['incident_title']} affected {telemetry.get('service', 'unknown')} with p95 latency {telemetry.get('p95_latency_ms')} ms, error rate {telemetry.get('error_rate_pct')}%, and retry count {telemetry.get('retry_count')}.",
        "probable_cause_hypothesis": hypothesis,
        "evidence_used": evidence,
        "missing_evidence": missing,
        "recommended_support_actions": actions,
        "escalation_recommendation": "escalate" if not runbooks or telemetry.get("error_rate_pct", 0) >= 4 else "hold_for_observation"
    }


def evaluate_summary(scenario, summary):
    summary_text = json.dumps(summary).lower()
    expected_actions = scenario.get("expected_actions", [])

    groundedness = bool(summary["evidence_used"])
    unsupported_detail_risk = "certain root cause" in summary_text or "definitely caused" in summary_text
    actionability = has_any(summary_text, expected_actions)
    uses_logs_or_runbook_context = bool(summary.get("evidence_used"))
    root_cause_as_hypothesis = "hypothesis" in summary["probable_cause_hypothesis"].lower()

    score = sum([
        groundedness,
        not unsupported_detail_risk,
        actionability,
        uses_logs_or_runbook_context,
        root_cause_as_hypothesis,
    ])

    return {
        "scenario_id": scenario["scenario_id"],
        "groundedness": groundedness,
        "unsupported_detail_risk": unsupported_detail_risk,
        "actionability": actionability,
        "uses_logs_or_runbook_context": uses_logs_or_runbook_context,
        "root_cause_framed_as_hypothesis": root_cause_as_hypothesis,
        "quality_score": score,
        "max_score": 5,
        "pass": score >= 4 and not unsupported_detail_risk
    }


def main():
    data = json.loads(Path("aiops_incident_triage/telemetry_triage_scenarios.json").read_text())
    results = []

    for scenario in data["scenarios"]:
        summary = generate_summary(scenario)
        evaluation = evaluate_summary(scenario, summary)
        results.append({
            "scenario_id": scenario["scenario_id"],
            "summary": summary,
            "evaluation": evaluation
        })

    report = {
        "total_scenarios": len(results),
        "passed": sum(1 for item in results if item["evaluation"]["pass"]),
        "failed": sum(1 for item in results if not item["evaluation"]["pass"]),
        "average_quality_score": round(sum(item["evaluation"]["quality_score"] for item in results) / len(results), 2),
        "results": results
    }

    Path("aiops_incident_triage/incident_triage_results.json").write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
