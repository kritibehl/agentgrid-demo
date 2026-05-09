from dataclasses import dataclass, asdict
from enum import Enum
from time import time
from uuid import uuid4
from typing import Dict, Optional, List


class JobStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    DEAD_LETTERED = "dead_lettered"


@dataclass
class ValidationJob:
    job_id: str
    input_text: str
    status: JobStatus
    attempts: int
    max_attempts: int
    created_at: float
    updated_at: float
    result: Optional[dict] = None
    error: Optional[str] = None


JOBS: Dict[str, ValidationJob] = {}
QUEUE: List[str] = []
DEAD_LETTER_QUEUE: List[str] = []


def enqueue_validation_job(input_text: str, max_attempts: int = 3) -> dict:
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
    JOBS[job.job_id] = job
    QUEUE.append(job.job_id)
    return asdict(job)


def get_job(job_id: str) -> Optional[dict]:
    job = JOBS.get(job_id)
    return asdict(job) if job else None


def list_jobs() -> List[dict]:
    return [asdict(job) for job in JOBS.values()]


def list_dead_letters() -> List[dict]:
    return [asdict(JOBS[job_id]) for job_id in DEAD_LETTER_QUEUE if job_id in JOBS]
