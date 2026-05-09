# Redis-Backed Async Validation Worker

AgentGrid includes a Redis-backed validation queue for GenAI support workflows.

## Flow

```text
POST /redis/jobs/validation
→ job stored in Redis
→ job ID pushed to Redis queue
→ worker processes validation
→ completed job stores result + trace + eval gate
→ failed job retries
→ exhausted retries move to Redis dead-letter queue
Endpoints
Endpoint	Purpose
GET /redis/health	Redis queue health
POST /redis/jobs/validation	Create Redis-backed validation job
GET /redis/jobs/{job_id}	Inspect job status
GET /redis/jobs	List jobs
POST /redis/workers/process-next	Process one Redis job
POST /redis/workers/process-until-idle	Drain pending Redis jobs
GET /redis/dead-letter	Inspect Redis dead-letter queue
Local Redis
docker run --name agentgrid-redis -p 6379:6379 -d redis:7
export REDIS_URL=redis://localhost:6379/0
Example
curl -X POST http://localhost:8000/redis/jobs/validation \
  -H "Content-Type: application/json" \
  -d '{"input":"Deployment failed because DB timeout caused retry storm.","max_attempts":3}'
curl -X POST http://localhost:8000/redis/workers/process-until-idle
Dead-Letter Proof
curl -X POST http://localhost:8000/redis/jobs/validation \
  -H "Content-Type: application/json" \
  -d '{"input":"FORCE_WORKER_FAILURE","max_attempts":2}'
curl -X POST http://localhost:8000/redis/workers/process-until-idle
curl http://localhost:8000/redis/dead-letter
Scope

This proves Redis-backed queueing, job-status tracking, retries, and dead-letter handling for support-validation workflows. It is still a local/development Redis deployment, not a managed production Redis service.
