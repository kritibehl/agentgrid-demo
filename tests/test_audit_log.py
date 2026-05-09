from src.audit.audit_log import AUDIT_EVENTS, record_audit_event, list_audit_events


def setup_function():
    AUDIT_EVENTS.clear()


def test_records_audit_event():
    event = record_audit_event(
        actor_id="reviewer_1",
        actor_role="reviewer",
        action="approve_decision",
        decision_id="decision_1",
        trace_id="trace_1",
        outcome="allowed",
        reason="allowed",
    )

    assert event["audit_id"].startswith("audit_")
    assert event["actor_role"] == "reviewer"
    assert event["outcome"] == "allowed"


def test_filters_audit_events_by_role():
    record_audit_event("u1", "reviewer", "approve_decision", "d1", "t1", "allowed", "allowed")
    record_audit_event("u2", "engineer", "create_bug_report", "d2", "t2", "allowed", "allowed")

    events = list_audit_events(actor_role="engineer")

    assert len(events) == 1
    assert events[0]["actor_role"] == "engineer"


def test_filters_audit_events_by_trace():
    record_audit_event("u1", "reviewer", "approve_decision", "d1", "trace_target", "allowed", "allowed")
    record_audit_event("u2", "engineer", "create_bug_report", "d2", "trace_other", "allowed", "allowed")

    events = list_audit_events(trace_id="trace_target")

    assert len(events) == 1
    assert events[0]["trace_id"] == "trace_target"
