from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from uuid import uuid4
from typing import List, Optional


@dataclass
class AuditEvent:
    audit_id: str
    actor_id: str
    actor_role: str
    action: str
    decision_id: str
    trace_id: str
    outcome: str
    reason: str
    created_at: str


AUDIT_EVENTS: List[AuditEvent] = []


def record_audit_event(
    actor_id: str,
    actor_role: str,
    action: str,
    decision_id: str,
    trace_id: str,
    outcome: str,
    reason: str,
) -> dict:
    event = AuditEvent(
        audit_id=f"audit_{uuid4().hex[:12]}",
        actor_id=actor_id,
        actor_role=actor_role,
        action=action,
        decision_id=decision_id,
        trace_id=trace_id,
        outcome=outcome,
        reason=reason,
        created_at=datetime.now(timezone.utc).isoformat(),
    )
    AUDIT_EVENTS.append(event)
    return asdict(event)


def list_audit_events(
    decision_id: Optional[str] = None,
    trace_id: Optional[str] = None,
    actor_role: Optional[str] = None,
) -> List[dict]:
    events = AUDIT_EVENTS

    if decision_id:
        events = [e for e in events if e.decision_id == decision_id]

    if trace_id:
        events = [e for e in events if e.trace_id == trace_id]

    if actor_role:
        events = [e for e in events if e.actor_role == actor_role]

    return [asdict(e) for e in events]
