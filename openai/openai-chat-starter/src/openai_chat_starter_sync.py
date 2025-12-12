import argparse
import os
import time

from openai import OpenAI


def main(model: str, base_url: str, api_key: str):
    t_0 = time.time()
    client = OpenAI(base_url=base_url, api_key=api_key)

    # Questions to test logical thinking about parallel processing
    questions = """
It has become commonplace for robots to wear clothes.
Robots won't make the mistake of putting on clothes inside out.

The robot will run two tasks in parallel and, once both tasks have completed
- regardless of whether they succeeded or failed - it will go shopping. Because it is in a hurry,
 it will not retry the failed parallel task.
The task is to pick up underwear or jeans and then put them on.
The actions of "picking up clothes" and "putting on what you have" are not atomic,
meaning that another task may interleave between them.

Parallel Task 1: 
(1) The robot picks up his underwear, and then
(2) puts it on if the robot holding his underwear, otherwise do nothing.
If the condition for putting on the clothing is not met,
the robot will skip that step and proceed without retrying.

Parallel Task 2: 
(1) The robot picks up his jeans, and then
(2) if he is wearing underwear and has jeans in his hand, it puts them on;
otherwise, it does nothing. If the condition for putting on the clothing is not met,
the robot will skip that step and proceed without retrying.

Please briefly explain the possible states of the robot after it leaves the room
 as a result of parallel processing.
 Also, please briefly explain the actions of the mall security guard in each state.
    """
    print(f"Question: {questions}")
    chat_completion = client.chat.completions.create(
        model=model,
        n=3,  # This parameter is ignored for llama3.2 models at least as of 2025-12-11.
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": "Limit your answer to one short sentence.",
            },
            {
                "role": "user",
                "content": questions,
            },
        ],
    )
    t_1 = time.time()
    time_delta = t_1 - t_0
    print(f"Response({time_delta:.1f}[s]):")
    cnt = 0
    print(chat_completion)
    for choice in chat_completion.choices:
        print(choice)
        # finish_reason: stop or length
        print(
            (
                f"choice[{cnt}]:finish_reason={choice.finish_reason},"
                f" tool_calls={choice.message.tool_calls}: "
            ),
            end="",
        )
        print(choice.message.content)
        cnt += 1


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
    main(args.model, args.base_url, args.api_key)
