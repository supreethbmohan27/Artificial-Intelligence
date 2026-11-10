
import argparse

from src.providers.openai_client import OpenAIClient
from src.providers.anthropic_client import AnthropicClient
from src.metrics import calculate_model_cost

def main():
    parser = argparse.ArgumentParser(
        description="Compare OpenAI and Anthropic LLM responses"
    )

    parser.add_argument(
        "prompt",
        help="Prompt to send to both LLMs"
    )

    parser.add_argument(
        "--system",
        default=None,
        help="Optional system prompt"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate inputs without calling APIs"
    )


    parser.add_argument(
        "--stream",
        action="store_true",
        help="Stream responses from both LLM providers"
    )

    args = parser.parse_args()

    if not args.prompt.strip():
        parser.error("Prompt cannot be empty.")

    if args.dry_run:
        print("\n========== DRY RUN ==========")
        print(f"User prompt: {args.prompt}")
        print(f"System prompt: {args.system or 'None'}")
        print("Providers: OpenAI, Anthropic")
        print("No API requests were made.")
        print(f"Streaming: {'Enabled' if args.stream else 'Disabled'}")

        return

    providers = [
        OpenAIClient(),
        AnthropicClient()
    ]

    
    for provider in providers:
        print(f"\n========== {provider.model} ==========")

        try:
            if args.stream:
                print("\nResponse:\n")

                
                result = provider.stream_response(
                    prompt=args.prompt,
                    system_prompt=args.system
                )

                cost = calculate_model_cost(
                    result["model"],
                    result["input_tokens"],
                    result["output_tokens"]
                )

                if cost is not None:
                    print(f"Estimated cost: ${cost:.6f}")
                else:
                    print("Estimated cost: unavailable")

                print("\n")
                print(f"Input tokens: {result['input_tokens']}")
                print(f"Output tokens: {result['output_tokens']}")
                print(f"Latency: {result['latency_seconds']}s")
                print(f"Time to first text: {result['ttft_seconds']}s")


                print()

            else:
                result = provider.generate_response(
                    prompt=args.prompt,
                    system_prompt=args.system
                )

                cost = calculate_model_cost(
                    result["model"],
                    result["input_tokens"],
                    result["output_tokens"]
                )

                print(f"Estimated cost: ${cost:.6f}")

                print(f"\n{result['response']}")
                print(
                    f"\nInput tokens: {result['input_tokens']}"
                )
                print(
                    f"Output tokens: {result['output_tokens']}"
                )
                print(
    f"Latency: {result['latency_seconds']} seconds"
)

        except Exception as error:
            print(
                f"Request failed: "
                f"{type(error).__name__}: {error}"
            )



if __name__ == "__main__":
    main()
