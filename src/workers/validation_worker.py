from time import time
from src.agent.graph import run_agent
from src.evals.evaluator import evaluate
from src.metrics.metrics import measure
from src.metrics.llm_metrics import build_llm_metrics
from src.observability.tracing import new_trace_context
from src.workers.job_queue import JOBS, QUEUE, DEAD_LETTER_QUEUE, JobStatus


EXPECTED_CONTEXT_COUNT = 3


def process_next_job() -> dict:
    if not QUEUE:
        return {"status": "idle", "message": "no pending jobs"}

    job_id = QUEUE.pop(0)
    job = JOBS[job_id]
    job.status = JobStatus.RUNNING
    job.updated_at = time()
    job.attempts += 1

    try:
        if "FORCE_WORKER_FAILURE" in job.input_text:
            raise RuntimeError("forced worker failure for dead-letter validation")

        output, latency = measure(run_agent, job.input_text)

        llm_metrics = build_llm_metrics(
            input_text=job.input_text,
            answer=output.get("answer", ""),
            latency_seconds=latency,
            retrieved_count=len(output.get("context", [])),
            expected_context_count=EXPECTED_CONTEXT_COUNT,
            trace_depth=len(output.get("trace", [])),
        )

        evals = evaluate(output, retrieval_hit_rate=llm_metrics["retrieval_hit_rate"])
        trace_context = new_trace_context(scenario_id=output.get("issue", "unknown"))

        job.status = JobStatus.COMPLETED
        job.result = {
            "agent_output": output,
            "trace": trace_context,
            "metrics": {
                "local_mock_latency_ms": round(latency * 1000, 2),
                "tool_call_success_rate": 0.0 if output.get("tool_errors") else 1.0,
                **llm_metrics,
            },
            "eval_gate": evals,
        }
        job.error = None

    except Exception as exc:
        job.error = str(exc)

        if job.attempts >= job.max_attempts:
            job.status = JobStatus.DEAD_LETTERED
            DEAD_LETTER_QUEUE.append(job.job_id)
        else:
            job.status = JobStatus.FAILED
            QUEUE.append(job.job_id)

    job.updated_at = time()
    return {
        "job_id": job.job_id,
        "status": job.status,
        "attempts": job.attempts,
        "error": job.error,
        "dead_lettered": job.job_id in DEAD_LETTER_QUEUE,
    }


def process_until_idle(limit: int = 20) -> dict:
    processed = []
    for _ in range(limit):
        result = process_next_job()
        processed.append(result)
        if result.get("status") == "idle":
            break

    return {
        "processed": processed,
        "dead_letters": len(DEAD_LETTER_QUEUE),
    }
