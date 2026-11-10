
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from src.providers.openai_client import OpenAIClient
from src.providers.anthropic_client import AnthropicClient
from src.metrics import calculate_model_cost


BASE_DIR = Path(__file__).resolve().parent
PROMPTS_FILE = BASE_DIR / "data" / "benchmark_prompts.json"
RESULTS_FILE = BASE_DIR / "results" / "comparison_results.json"


def load_prompts():
    with open(PROMPTS_FILE, "r", encoding="utf-8") as file:
        prompts = json.load(file)

    if not isinstance(prompts, list) or len(prompts) != 10:
        raise ValueError("Benchmark must contain exactly 10 prompts.")

    for item in prompts:
        if not all(key in item for key in ("id", "category", "prompt")):
            raise ValueError("Each prompt needs id, category and prompt.")

    return prompts


def save_results(results):
    RESULTS_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(RESULTS_FILE, "w", encoding="utf-8") as file:
        json.dump(results, file, indent=2, ensure_ascii=False)


def run_benchmark(dry_run=False):
    prompts = load_prompts()

    if dry_run:
        print(f"Loaded {len(prompts)} benchmark prompts.")
        print("Providers: OpenAI, Anthropic")
        print("Expected requests: 20")
        print("Dry run completed. No API requests were made.")
        return

    providers = [OpenAIClient(), AnthropicClient()]
    results = []

    for item in prompts:
        print(f"\nPrompt {item['id']}: {item['category']}")

        for provider in providers:
            print(f"Running {provider.model}...")

            record = {
                "prompt_id": item["id"],
                "category": item["category"],
                "prompt": item["prompt"],
                "provider": provider.__class__.__name__,
                "model": provider.model,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

            try:
                response = provider.generate_response(
                    prompt=item["prompt"]
                )

                cost = calculate_model_cost(
                    response["model"],
                    response["input_tokens"],
                    response["output_tokens"],
                )

                record.update({
                    "status": "success",
                    "response": response["response"],
                    "input_tokens": response["input_tokens"],
                    "output_tokens": response["output_tokens"],
                    "latency_seconds": response["latency_seconds"],
                    "estimated_cost_usd": cost,
                })

            except Exception as error:
                record.update({
                    "status": "error",
                    "error_type": type(error).__name__,
                    "error": str(error),
                })

            results.append(record)

            # Preserve progress after every request.
            save_results(results)

    print(f"\nBenchmark completed: {len(results)} records.")
    print(f"Results saved to: {RESULTS_FILE}")


def main():
    parser = argparse.ArgumentParser(
        description="Benchmark OpenAI and Anthropic models"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate benchmark without API requests",
    )

    args = parser.parse_args()
    run_benchmark(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
