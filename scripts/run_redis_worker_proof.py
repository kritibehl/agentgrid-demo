import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.workers.redis_job_queue import enqueue_redis_validation_job, get_redis_job, redis_health, list_redis_dead_letters
from src.workers.redis_validation_worker import process_redis_until_idle


def main():
    print(json.dumps({"redis_health": redis_health()}, indent=2))

    success_job = enqueue_redis_validation_job(
        "Deployment failed because DB timeout caused retry storm.",
        max_attempts=3,
    )

    failed_job = enqueue_redis_validation_job(
        "FORCE_WORKER_FAILURE",
        max_attempts=2,
    )

    result = process_redis_until_idle(limit=10)

    proof = {
        "processed": result,
        "success_job": get_redis_job(success_job["job_id"]),
        "failed_job": get_redis_job(failed_job["job_id"]),
        "dead_letters": list_redis_dead_letters(),
    }

    out = Path("reports/platform_proof/redis_worker_proof.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(proof, indent=2))

    print(json.dumps(proof, indent=2))


if __name__ == "__main__":
    main()
