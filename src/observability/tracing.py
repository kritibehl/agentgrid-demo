from datetime import datetime, timezone
from uuid import uuid4

def new_trace_context(scenario_id="unknown", prompt_version="prompt_v1", retrieval_version="retrieval_v1"):
    run_id = f"run_{uuid4().hex[:12]}"
    return {
        "trace_id": f"trace_{uuid4().hex[:16]}",
        "run_id": run_id,
        "scenario_id": scenario_id,
        "decision_id": f"decision_{uuid4().hex[:12]}",
        "prompt_version": prompt_version,
        "retrieval_version": retrieval_version,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
