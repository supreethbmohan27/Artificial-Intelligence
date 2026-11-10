
import time
from src.pricing import get_model_pricing

def calculate_latency(start_time):
    """Return elapsed time in seconds."""
    return round(time.perf_counter() - start_time, 3)


def calculate_cost(
    input_tokens,
    output_tokens,
    input_price_per_million,
    output_price_per_million
):
    """Estimate API cost in USD."""

    input_cost = (
        input_tokens / 1_000_000
    ) * input_price_per_million

    output_cost = (
        output_tokens / 1_000_000
    ) * output_price_per_million

    return round(input_cost + output_cost, 8)


def calculate_model_cost(model, input_tokens, output_tokens):
    """Estimate model cost using configured pricing."""

    if input_tokens is None or output_tokens is None:
        return None

    pricing = get_model_pricing(model)

    return calculate_cost(
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        input_price_per_million=pricing["input"],
        output_price_per_million=pricing["output"],
    )
