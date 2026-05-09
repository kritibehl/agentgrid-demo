import json
import os
from dataclasses import asdict
from time import time
from uuid import uuid4
from typing import Optional, List

import redis

from src.workers.job_queue import ValidationJob, JobStatus


REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
JOB_PREFIX = "agentgrid:job:"
QUEUE_KEY = "agentgrid:validation_queue"
DLQ_KEY = "agentgrid:dead_letter_queue"


def get_redis():
    return redis.Redis.from_url(REDIS_URL, decode_responses=True)


def _job_key(job_id: str) -> str:
    return f"{JOB_PREFIX}{job_id}"


def _serialize(job: ValidationJob) -> str:
    data = asdict(job)
    data["status"] = str(job.status.value if hasattr(job.status, "value") else job.status)
    return json.dumps(data)


def _deserialize(raw: str) -> dict:
    return json.loads(raw)


def enqueue_redis_validation_job(input_text: str, max_attempts: int = 3) -> dict:
    now = time()
    job = ValidationJob(
        job_id=f"job_{uuid4().hex[:12]}",
        input_text=input_text,
        status=JobStatus.PENDING,
        attempts=0,
        max_attempts=max_attempts,
        created_at=now,
        updated_at=now,
    )

    r = get_redis()
    r.set(_job_key(job.job_id), _serialize(job))
    r.rpush(QUEUE_KEY, job.job_id)

    return _deserialize(_serialize(job))


def get_redis_job(job_id: str) -> Optional[dict]:
    raw = get_redis().get(_job_key(job_id))
    return _deserialize(raw) if raw else None


def save_redis_job(job: dict) -> dict:
    get_redis().set(_job_key(job["job_id"]), json.dumps(job))
    return job


def pop_next_redis_job() -> Optional[dict]:
    r = get_redis()
    job_id = r.lpop(QUEUE_KEY)
    if not job_id:
        return None
    return get_redis_job(job_id)


def requeue_redis_job(job_id: str) -> None:
    get_redis().rpush(QUEUE_KEY, job_id)


def dead_letter_redis_job(job_id: str) -> None:
    get_redis().rpush(DLQ_KEY, job_id)


def list_redis_dead_letters() -> List[dict]:
    r = get_redis()
    ids = r.lrange(DLQ_KEY, 0, -1)
    return [job for job_id in ids if (job := get_redis_job(job_id))]


def list_redis_jobs() -> List[dict]:
    r = get_redis()
    keys = r.keys(f"{JOB_PREFIX}*")
    jobs = []
    for key in keys:
        raw = r.get(key)
        if raw:
            jobs.append(_deserialize(raw))
    return sorted(jobs, key=lambda item: item.get("created_at", 0), reverse=True)


def redis_health() -> dict:
    r = get_redis()
    pong = r.ping()
    return {
        "redis_url": REDIS_URL,
        "healthy": bool(pong),
        "queue_depth": r.llen(QUEUE_KEY),
        "dead_letter_depth": r.llen(DLQ_KEY),
    }
