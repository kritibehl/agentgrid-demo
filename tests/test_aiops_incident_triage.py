import json
from pathlib import Path

from aiops_incident_triage.run_incident_triage_eval import generate_summary, evaluate_summary


def test_incident_triage_outputs_hypothesis():
    scenario = json.loads(Path("aiops_incident_triage/telemetry_triage_scenarios.json").read_text())["scenarios"][0]
    summary = generate_summary(scenario)

    assert "hypothesis" in summary["probable_cause_hypothesis"].lower()
    assert summary["recommended_support_actions"]


def test_incident_triage_quality_passes():
    scenario = json.loads(Path("aiops_incident_triage/telemetry_triage_scenarios.json").read_text())["scenarios"][0]
    summary = generate_summary(scenario)
    evaluation = evaluate_summary(scenario, summary)

    assert evaluation["pass"] is True
    assert evaluation["unsupported_detail_risk"] is False
