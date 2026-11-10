
import pytest

from src.metrics import calculate_cost, calculate_model_cost
from src.pricing import get_model_pricing


def test_basic_cost_calculation():
    cost = calculate_cost(
        input_tokens=1000,
        output_tokens=500,
        input_price_per_million=1.0,
        output_price_per_million=4.0
    )

    assert cost == 0.003


def test_openai_model_cost():
    cost = calculate_model_cost(
        "gpt-4.1-mini", 1000, 500
    )

    assert cost == 0.0012


def test_anthropic_model_cost():
    cost = calculate_model_cost(
        "claude-sonnet-4-5", 1000, 500
    )

    assert cost == 0.0105


def test_missing_token_usage():
    cost = calculate_model_cost(
        "gpt-4.1-mini", None, None
    )

    assert cost is None


def test_unknown_model():
    with pytest.raises(ValueError):
        get_model_pricing("unknown-model")
