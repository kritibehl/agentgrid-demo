import re
import time

INPUT_TOKEN_COST_PER_1K = 0.0005
OUTPUT_TOKEN_COST_PER_1K = 0.0015

def estimate_tokens(text: str) -> int:
    # Simple local estimator: roughly word/punctuation tokens.
    return max(1, len(re.findall(r"\w+|[^\w\s]", text)))

def build_llm_metrics(input_text: str, answer: str, latency_seconds: float, retrieved_count: int, expected_context_count: int, trace_depth: int):
    tokens_input = estimate_tokens(input_text)
    tokens_output = estimate_tokens(answer)

    total_tokens = tokens_input + tokens_output
    tokens_per_second = round(total_tokens / max(latency_seconds, 0.0001), 2)

    estimated_cost = (
        (tokens_input / 1000) * INPUT_TOKEN_COST_PER_1K
        + (tokens_output / 1000) * OUTPUT_TOKEN_COST_PER_1K
    )

    retrieval_hit_rate = retrieved_count / max(expected_context_count, 1)

    return {
        "tokens_input": tokens_input,
        "tokens_output": tokens_output,
        "tokens_per_second": tokens_per_second,
        "estimated_cost_per_request": round(estimated_cost, 6),
        "retrieval_hit_rate": round(retrieval_hit_rate, 2),
        "trace_depth": trace_depth,
    }
