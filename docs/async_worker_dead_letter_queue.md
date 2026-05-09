# Async Validation Worker and Dead-Letter Queue

AgentGrid includes a local async validation-worker model for support-validation workflows.

## Flow

```text
POST /jobs/validation
→ job queued as pending
→ worker processes validation
→ job becomes completed or failed
→ retries until max_attempts
→ failed jobs move to dead-letter queue
Endpoints
Endpoint	Purpose
POST /jobs/validation	create validation job
GET /jobs/{job_id}	inspect job status
GET /jobs	list validation jobs
POST /workers/process-next	process one job
POST /workers/process-until-idle	drain pending queue
GET /dead-letter	inspect dead-lettered jobs
Failure Test

Use this input to force a dead-letter path:

FORCE_WORKER_FAILURE
Scope

This is an in-memory worker and queue model. It proves async workflow design, retry states, job-status tracking, and dead-letter handling. It is not a Redis deployment yet.
