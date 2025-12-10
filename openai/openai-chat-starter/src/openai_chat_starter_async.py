import argparse
import asyncio
import os

from openai import AsyncOpenAI


async def main(model: str, base_url: str, api_key: str) -> None:
    async with AsyncOpenAI(
        base_url=base_url,
        api_key=api_key,
    ) as client:
        chat_completion_stream = await client.chat.completions.create(
            stream=True,
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are an assistant who prefers concise answers,"
                    " typically one sentence.",
                },
                {"role": "user", "content": "What is the tallest mountain in the world?"},
            ],
        )
        async for event in chat_completion_stream:
            # In stream mode, the number of elements in choices is always 1.
            choice = event.choices[0]
            if choice.finish_reason and choice.finish_reason == "stop":
                print("")
                break
            print(choice.delta.content, end="", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Send a simple chat request to an OpenAI server or an OpenAI-compatible server."
    )
    parser.add_argument("-m", "--model", default=os.environ.get("MODEL"), help="Model name to use.")

    parser.add_argument(
        "--base-url",
        default=os.environ.get("OPENAI_BASE_URL", ""),
        help="base url of the OpenAI server. ",
    )
    parser.add_argument(
        "--api-key",
        default=os.environ.get("OPENAI_API_KEY", ""),
        help="API Key for the OpenAI server. ",
    )
    args = parser.parse_args()
    asyncio.run(main(args.model, args.base_url, args.api_key))
