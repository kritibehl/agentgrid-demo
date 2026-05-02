import json
from datetime import datetime, timezone
from pathlib import Path

EVENTS_PATH = Path("events/autoops_events.jsonl")

def emit_autoops_event(source: str, issue_type: str, severity: str, decision: str, reason: str):
    EVENTS_PATH.parent.mkdir(exist_ok=True)

    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "source": source,
        "issue_type": issue_type,
        "severity": severity,
        "decision": decision,
        "reason": reason,
    }

    with EVENTS_PATH.open("a") as f:
        f.write(json.dumps(event) + "\n")

    return event
