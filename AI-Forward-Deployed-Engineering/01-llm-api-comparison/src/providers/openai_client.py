
import os
import time
from dotenv import load_dotenv
from openai import OpenAI

from src.metrics import calculate_cost

load_dotenv()


class OpenAIClient:
    def __init__(self, model="gpt-4.1-mini"):
        self.model = model
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )


    def generate_response(self, prompt, system_prompt=None):
        messages = []

        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })

        messages.append({
            "role": "user",
            "content": prompt
        })

        start_time = time.perf_counter()

        response = self.client.responses.create(
            model=self.model,
            input=messages
        )

        latency = round(
            time.perf_counter() - start_time, 3
        )

        return {
            "provider": "OpenAI",
            "model": self.model,
            "response": response.output_text,
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens,
            "latency_seconds": latency
        }

  
    
    def stream_response(self, prompt, system_prompt=None):
        messages = []

        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })

        messages.append({
            "role": "user",
            "content": prompt
        })

        start_time = time.perf_counter()
        first_token_time = None
        response_chunks = []
        input_tokens = None
        output_tokens = None

        stream = self.client.responses.create(
            model=self.model,
            input=messages,
            stream=True
        )

        for event in stream:
            if event.type == "response.output_text.delta":
                if first_token_time is None:
                    first_token_time = time.perf_counter()

                response_chunks.append(event.delta)
                print(event.delta, end="", flush=True)

            elif event.type == "response.completed":
                usage = event.response.usage
                if usage:
                    input_tokens = usage.input_tokens
                    output_tokens = usage.output_tokens

        total_latency = time.perf_counter() - start_time

        return {
            "provider": "OpenAI",
            "model": self.model,
            "response": "".join(response_chunks),
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "latency_seconds": round(total_latency, 3),
            "ttft_seconds": (
                round(first_token_time - start_time, 3)
                if first_token_time is not None
                else None
            )
        }
