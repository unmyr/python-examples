import argparse
import json
import os
# import random
import time

from openai import OpenAI


def collatz(n: int) -> int:
    # If the number is even, divide it by 2
    if n % 2 == 0:
        return n // 2
    else:
        # If the number is odd, multiply by 3 and add 1
        return 3 * n + 1


def main(model: str, base_url: str, api_key: str):
    # 53 → 160 → 80 → 40 → 20 → 10 → 5 → 16 → 8 → 4 → 2 → 1
    n = 53  # random.randint(2, 99)

    available_functions = {"collatz": collatz}
    param_types = {"collatz": {"n": int}}

    client = OpenAI(base_url=base_url, api_key=api_key)
    tool_collatz = {
        "type": "function",
        "function": {
            "name": "collatz",
            "description": (
                "Given a positive integer n>1, return the next number in the Collatz sequence."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "n": {
                        "type": "integer",
                        "description": "A positive integer input for the Collatz function.",
                    }
                },
                "required": ["n"],
            },
        },
    }
    series_n = [n]
    system_prompt = (
        "You are an assistant who can call functions repeatedly to complete a task."
        " Be concise, but complete the full process when asked."
        " Be concise, complete the entire process when prompted,"
        " but exit when the collatz function responds with a 1."
    )
    input_list = [
        {
            "role": "system",
            "content": system_prompt,
        },
        {
            "role": "user",
            "content": (
                f"Call the collatz function repeatedly, starting with {n},"
                " until the result is 1. Continue calling the function with each new result."
            ),
        },
    ]
    print(f"Model: {model}")
    stop = False
    for r_i in range(1, 99):
        print()
        if stop:
            print("INFO: A stop notification has been detected. Chat will end.")
            break

        print(f"Request[{r_i}]:")
        for message in input_list:
            print(f"message: {message}")
        print()

        t_0 = time.time()
        chat_completion = client.chat.completions.create(
            model=model,
            messages=input_list,
            tools=[tool_collatz],
            stream=False,
        )
        t_1 = time.time()
        elapsed_time = t_1 - t_0
        tps = chat_completion.usage.completion_tokens / elapsed_time
        print(
            (
                f"Response({elapsed_time:.1f}[s], {tps:.2f} [token/s]): id={chat_completion.id}"
                " series={series_n}"
            )
        )
        # print(f"chat_completion={chat_completion}")

        for choice in chat_completion.choices:
            print(
                (
                    f"choice[{choice.index}]:"
                    f" finish_reason={choice.finish_reason},"
                    f" role={choice.message.role},"
                    f" function_call={choice.message.function_call},"
                    f" refusal={choice.message.refusal},"
                    f" tool_calls={choice.message.tool_calls}:"
                )
            )
            # print(f"choice[{choice.index}]={choice}")
            if choice.finish_reason == "stop":
                content = choice.message.content
                print(content)
                if series_n[-1] == 1:
                    # We reach the stopping condition for the Collatz function
                    stop = True
                    continue

                last_value = series_n[-1]
                last_seq = " → ".join(map(str, series_n))
                resume_message = (
                    "Resume the Collatz sequence using the last result."
                    f" The Collatz sequence so far is: {last_seq}."
                    f" Please continue calling the collatz function starting from {last_value}"
                    " until the result is 1."
                )
                input_list = [
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {
                        "role": "user",
                        "content": resume_message,
                    },
                ]

            elif choice.finish_reason == "tool_calls":
                tool_caller = []

                # Append tool_call requests to input_list
                for _, tool_call in enumerate(choice.message.tool_calls):
                    # print(f"tool_call={tool_call}")
                    tool_caller.append(
                        {
                            "index": tool_call.index,
                            "type": tool_call.type,
                            "id": tool_call.id,
                            "function": {
                                "name": tool_call.function.name,
                                "arguments": tool_call.function.arguments,
                            },
                        }
                    )

                print(f"tool_caller={tool_caller}")
                input_list.append(
                    {
                        "role": choice.message.role,
                        "content": choice.message.content,
                        "tool_calls": tool_caller,
                    }
                )

                for tool_call in choice.message.tool_calls:
                    f_name = tool_call.function.name
                    f_arguments = json.loads(tool_call.function.arguments)
                    if f_name in available_functions:
                        expected_type = param_types[f_name]
                        f_arguments_converted = {
                            k: expected_type[k](v) if k in expected_type else v
                            for k, v in f_arguments.items()
                        }
                        try:
                            print(f"f_arguments={f_arguments}, series={series_n[-2:]}")
                            output = available_functions[f_name](**f_arguments_converted)
                            if f_arguments_converted.get("n") == 1:
                                input_list.append(
                                    {
                                        "role": "tool",
                                        "tool_call_id": tool_call.id,
                                        "name": f_name,
                                        "content": json.dumps(
                                            {
                                                "error": (
                                                    "The function call condition is an integer"
                                                    " greater than 1."
                                                )
                                            }
                                        ),
                                    }
                                )
                            elif series_n[-1] != f_arguments_converted.get("n"):
                                error_message = (
                                    "This is a calculated input value."
                                    f" Please calculate against the last value {series_n[-1]}."
                                )
                                input_list.append(
                                    {
                                        "role": "tool",
                                        "tool_call_id": tool_call.id,
                                        "name": f_name,
                                        "content": json.dumps({"error": error_message}),
                                    }
                                )
                            else:
                                series_n.append(output)
                                input_list.append(
                                    {
                                        "role": "tool",
                                        "tool_call_id": tool_call.id,
                                        "name": f_name,
                                        "content": json.dumps({"n": output}),
                                    }
                                )
                        except TypeError as exc:
                            print(str(exc))
                            input_list.append(
                                {
                                    "role": "tool",
                                    "tool_call_id": tool_call.id,
                                    "name": f_name,
                                    "content": json.dumps({"error": str(exc)}),
                                }
                            )

    print()
    print("Recording results of executions outside of LLM:")
    print(f"series_n={series_n}")


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
