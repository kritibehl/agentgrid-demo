import json
from collections import Counter
from pathlib import Path


DECISION_PRIORITY = {
    "deny_tool_call": 5,
    "require_human_review": 4,
    "escalate": 3,
    "hold": 2,
    "allow": 1
}


def load_rules(path="agent_governance/policy_rules.json"):
    return json.loads(Path(path).read_text())


def evaluate_run(run, rules_config=None):
    rules_config = rules_config or load_rules()
    signals = run.get("signals", {})
    triggered = []

    for rule in rules_config["rules"]:
        if signals.get(rule["signal"], False):
            triggered.append(rule)

    if not triggered:
        return {
            "run_id": run["run_id"],
            "policy_version": rules_config["policy_version"],
            "policy_decision": "allow",
            "triggered_rules": [],
            "tool_access": "allowed",
            "escalation_target": "none",
            "audit_required": False
        }

    selected = sorted(
        triggered,
        key=lambda rule: DECISION_PRIORITY[rule["decision"]],
        reverse=True
    )[0]

    return {
        "run_id": run["run_id"],
        "policy_version": rules_config["policy_version"],
        "policy_decision": selected["decision"],
        "triggered_rules": [rule["rule_id"] for rule in triggered],
        "tool_access": selected["tool_access"],
        "escalation_target": selected["escalation_target"],
        "audit_required": any(rule["audit_required"] for rule in triggered)
    }


def evaluate_file(input_path="agent_governance/governance_decision_examples.json"):
    runs = json.loads(Path(input_path).read_text())
    rules = load_rules()
    decisions = [evaluate_run(run, rules) for run in runs]

    decision_counts = Counter(item["policy_decision"] for item in decisions)
    rule_counts = Counter(rule for item in decisions for rule in item["triggered_rules"])

    report = {
        "total_agent_runs": len(decisions),
        "allow_count": decision_counts.get("allow", 0),
        "hold_count": decision_counts.get("hold", 0),
        "escalate_count": decision_counts.get("escalate", 0),
        "human_review_count": decision_counts.get("require_human_review", 0),
        "denied_tool_call_count": decision_counts.get("deny_tool_call", 0),
        "top_triggered_policy_rules": rule_counts.most_common(),
        "policy_decision_distribution": dict(decision_counts),
        "decisions": decisions
    }

    out = Path("agent_governance/policy_decision_report.json")
    out.write_text(json.dumps(report, indent=2))
    return report


def main():
    report = evaluate_file()
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
