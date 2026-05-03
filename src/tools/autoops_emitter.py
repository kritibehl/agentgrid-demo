import os
import requests

AUTOOPS_URL = os.getenv("AUTOOPS_URL", "")

def emit_autoops_event(source, issue_type, severity, decision, reason):
    event = {
        "source": source,
        "issue_type": issue_type,
        "severity": severity,
        "decision": decision,
        "reason": reason,
    }

    if not AUTOOPS_URL:
        return {"status": "skipped", "reason": "no AUTOOPS_URL set", "event": event}

    try:
        r = requests.post(f"{AUTOOPS_URL}/support/ingest", json=event, timeout=5)
        return {
            "status": "sent",
            "status_code": r.status_code,
            "response": r.text[:300],
            "event": event,
        }
    except Exception as e:
        return {"status": "error", "error": str(e), "event": event}
