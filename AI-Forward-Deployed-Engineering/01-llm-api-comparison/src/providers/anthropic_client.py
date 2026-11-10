
import os
import time
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()


class AnthropicClient:
    def __init__(self, model="claude-sonnet-4-5"):
        self.model = model
        self.client = Anthropic(
            api_key=os.getenv("ANTHROPIC_API_KEY")
        )

    
    def generate_response(self, prompt, system_prompt=None):
        request_params = {
            "model": self.model,
            "max_tokens": 1024,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }

        if system_prompt:
            request_params["system"] = system_prompt

        start_time = time.perf_counter()

        response = self.client.messages.create(
            **request_params
        )

        latency = round(
            time.perf_counter() - start_time, 3
        )

        response_text = "".join(
            block.text
            for block in response.content
            if block.type == "text"
        )

        return {
            "provider": "Anthropic",
            "model": self.model,
            "response": response_text,
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens,
            "latency_seconds": latency
        }


    
    def stream_response(self, prompt, system_prompt=None):
        request_params = {
            "model": self.model,
            "max_tokens": 1024,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }

        if system_prompt:
            request_params["system"] = system_prompt

        start_time = time.perf_counter()
        first_token_time = None
        response_chunks = []

        with self.client.messages.stream(
            **request_params
        ) as stream:
            for text in stream.text_stream:
                if first_token_time is None:
                    first_token_time = time.perf_counter()

                response_chunks.append(text)
                print(text, end="", flush=True)

            final_message = stream.get_final_message()

        total_latency = time.perf_counter() - start_time

        return {
            "provider": "Anthropic",
            "model": self.model,
            "response": "".join(response_chunks),
            "input_tokens": final_message.usage.input_tokens,
            "output_tokens": final_message.usage.output_tokens,
            "latency_seconds": round(total_latency, 3),
            "ttft_seconds": (
                round(first_token_time - start_time, 3)
                if first_token_time is not None
                else None
            )
        }
