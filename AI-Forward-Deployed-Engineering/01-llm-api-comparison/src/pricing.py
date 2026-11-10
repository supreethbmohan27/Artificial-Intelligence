
# USD per 1 million tokens.
# Illustrative rates only — replace with verified
# provider pricing before running live benchmarks.

MODEL_PRICING = {
    "gpt-4.1-mini": {
        "input": 0.40,
        "output": 1.60,
    },
    "claude-sonnet-4-5": {
        "input": 3.00,
        "output": 15.00,
    },
}


def get_model_pricing(model):
    """Return configured input/output rates."""
    if model not in MODEL_PRICING:
        raise ValueError(
            f"No pricing configured for model: {model}"
        )

    return MODEL_PRICING[model]
