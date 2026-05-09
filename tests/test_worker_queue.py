from src.workers.job_queue import enqueue_validation_job, get_job, DEAD_LETTER_QUEUE, JOBS, QUEUE
from src.workers.validation_worker import process_until_idle


def setup_function():
    JOBS.clear()
    QUEUE.clear()
    DEAD_LETTER_QUEUE.clear()


def test_validation_job_completes():
    job = enqueue_validation_job("Deployment failed because DB timeout caused retry storm.")
    result = process_until_idle()

    saved = get_job(job["job_id"])

    assert saved["status"] == "completed"
    assert saved["result"]["eval_gate"]["final_decision"] in ("ship", "hold", "escalate")
    assert "trace_id" in saved["result"]["trace"]


def test_failed_job_goes_to_dead_letter():
    job = enqueue_validation_job("FORCE_WORKER_FAILURE", max_attempts=2)
    process_until_idle(limit=5)

    saved = get_job(job["job_id"])

    assert saved["status"] == "dead_lettered"
    assert saved["attempts"] == 2
    assert len(DEAD_LETTER_QUEUE) == 1
