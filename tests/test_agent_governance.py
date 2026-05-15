from agent_governance.evaluate_policy_decision import evaluate_run, load_rules


def test_allows_clean_run():
    decision = evaluate_run(
        {
            "run_id": "clean",
            "signals": {
                "unsupported_detail_detected": False,
                "missing_retrieval_grounding": False,
                "policy_conflict": False,
                "sensitive_context_risk": False,
                "tool_call_failure": False,
                "high_cost_retry_loop": False,
                "insufficient_evidence": False
            }
        },
        load_rules()
    )

    assert decision["policy_decision"] == "allow"
    assert decision["tool_access"] == "allowed"
    assert decision["audit_required"] is False


def test_requires_human_review_for_sensitive_missing_grounding():
    decision = evaluate_run(
        {
            "run_id": "review",
            "signals": {
                "missing_retrieval_grounding": True,
                "sensitive_context_risk": True
            }
        },
        load_rules()
    )

    assert decision["policy_decision"] == "require_human_review"
    assert decision["tool_access"] == "restricted"
    assert decision["audit_required"] is True


def test_denies_tool_call_for_high_cost_retry_loop():
    decision = evaluate_run(
        {
            "run_id": "deny",
            "signals": {
                "high_cost_retry_loop": True,
                "insufficient_evidence": True
            }
        },
        load_rules()
    )

    assert decision["policy_decision"] == "deny_tool_call"
    assert decision["tool_access"] == "denied"
