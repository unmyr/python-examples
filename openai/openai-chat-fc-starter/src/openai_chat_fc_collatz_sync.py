import argparse
import json
import os
import random
import time

from openai import OpenAI


def int_greater_than(min_value, numeric_type=int):
    def validate(value):
        number = numeric_type(value)
        if number > min_value:
            return number
        raise argparse.ArgumentTypeError(
            f"Invalid value: {value}. Must be an integer greater than {min_value}."
        )

    return validate


def collatz(n: int) -> int:
    """Compute the next number in the Collatz sequence."""
    # Example:
    # 53 → 160 → 80 → 40 → 20 → 10 → 5 → 16 → 8 → 4 → 2 → 1
    if n < 2:
        raise ValueError(f"Input must be an integer greater than 1, but got {n}.")

    # If the number is even, divide it by 2
    if n % 2 == 0:
        return n // 2
    else:
        # If the number is odd, multiply by 3 and add 1
        return 3 * n + 1


def main(model: str, base_url: str, api_key: str, n: int):
    available_functions = {"collatz": collatz}
    param_types = {"collatz": {"n": int}}

    client = OpenAI(base_url=base_url, api_key=api_key)
    tool_collatz = {
        "type": "function",
        "function": {
            "name": "collatz",
            "description": (
                "If a positive integer n>1 is specified, an integer is returned. "
                "The returned integer value is expected to be used as input to this function again."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "n": {
                        "type": "integer",
                        "description": (
                            "A positive integer(>1) input for the Collatz function."
                            " Since the Collatz function is a recursive function,"
                            " an error will occur if the result of the previous execution"
                            " is not used as input from the second time onwards."
                        ),
                    }
                },
                "required": ["n"],
            },
        },
    }
    series_n = [n]
    system_prompt = (
        "You are an assistant who can call functions repeatedly to complete a task."
        " No guesses are made about the next value in the sequence."
        " However, if the collatz function returns 1, it will exit,"
        f" display the sequence from the first value {n} to the last, and then exit."
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
    tool_choice = "required"
    for r_i in range(1, 99):
        print()
        if stop:
            print("INFO: A stop notification has been detected. Chat will end.")
            break

        if series_n[-1] == 1:
            stop = True
            tool_choice = "none"

        print(f"Request[{r_i}]: tool_choice={tool_choice} series={series_n}")
        for message in input_list:
            print(f"message: {message}")
        print()

        t_0 = time.time()
        chat_completion = client.chat.completions.create(
            model=model,
            messages=input_list,
            tool_choice=tool_choice,
            tools=[tool_collatz],
            stream=False,
        )
        t_1 = time.time()
        elapsed_time = t_1 - t_0
        tps = chat_completion.usage.completion_tokens / elapsed_time
        print(
            (
                f"Response({elapsed_time:.1f}[s], {tps:.2f} [token/s]): id={chat_completion.id}"
                f" series={series_n}"
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
                first_value = series_n[0]
                last_value = series_n[-1]

                last_seq = " → ".join(map(str, series_n))
                resume_message = (
                    "Resume the Collatz sequence using the last result."
                    f" The Collatz sequence so far is: {last_seq}."
                    f" Please continue calling the collatz function without reporting anything"
                    f" starting from {last_value} until the result is 1."
                    " When the return value of the Collatz function is 1,"
                    f" print the sequence starting from {first_value} and stop."
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
                # Append tool_call requests to input_list
                tool_callers = []
                for i, tool_call in enumerate(choice.message.tool_calls):
                    # print(f"tool_call={tool_call}")
                    f_name = tool_call.function.name
                    if f_name not in available_functions:
                        input_list.append(
                            {
                                "role": "tool",
                                "tool_call_id": tool_call.id,
                                "name": f_name,
                                "content": json.dumps(
                                    {"error": "An undefined function call was detected."}
                                ),
                            }
                        )
                        continue

                    f_arguments = json.loads(tool_call.function.arguments)
                    expected_type = param_types[f_name]
                    f_arguments_converted = {
                        k: expected_type[k](v) if k in expected_type else v
                        for k, v in f_arguments.items()
                    }
                    n = f_arguments_converted.get("n")
                    if i > 0 and n != series_n[-1]:
                        # In the lightweight model, there is a tendency to ignore explicit rules and
                        # prioritize look-ahead, which can lead to frequent errors,
                        # so we filter out invalid calls from the second record onwards.
                        continue

                    tool_callers.append(
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

                input_list.append(
                    {
                        "role": choice.message.role,
                        "content": choice.message.content,
                        "tool_calls": tool_callers,
                    }
                )

                for tool_caller in tool_callers:
                    f_name = tool_caller.get("function").get("name")
                    f_arguments = json.loads(tool_caller.get("function").get("arguments"))
                    expected_type = param_types[f_name]
                    f_arguments_converted = {
                        k: expected_type[k](v) if k in expected_type else v
                        for k, v in f_arguments.items()
                    }
                    if f_name == "collatz":
                        try:
                            n = f_arguments_converted.get("n")
                            if n == series_n[-1]:
                                next_value = available_functions[f_name](**f_arguments_converted)
                                series_n.append(next_value)
                                if next_value == 1:
                                    tool_response = {
                                        "next_value": next_value,
                                        "sequence_so_far": series_n,
                                        "message": (
                                            "The termination conditions have been met."
                                            " Please end the chat."
                                        ),
                                        "done": True,
                                    }
                                else:
                                    tool_response = {
                                        "next_value": next_value,
                                        "sequence_so_far": series_n,
                                        "message": (
                                            "Call the collatz function again using a next value"
                                        ),
                                        "done": False,
                                    }

                            else:
                                error_message = (
                                    f"Calling any value other than the last value {series_n[-1]}"
                                    " in the Collatz sequence is invalid."
                                )
                                tool_response = {
                                    "next_value": None,
                                    "sequence_so_far": series_n,
                                    "error": error_message,
                                }

                        except ValueError as exc:
                            tool_response = {
                                "next_value": None,
                                "sequence_so_far": series_n,
                                "error": str(exc),
                            }

                        input_list.append(
                            {
                                "role": "tool",
                                "tool_call_id": tool_caller.get("id"),
                                "name": f_name,
                                "content": json.dumps(tool_response),
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
    parser.add_argument(
        "-n",
        default=random.randint(2, 99),
        help="Starting integer (>1) for the Collatz sequence.",
        type=int_greater_than(1),
    )

    args = parser.parse_args()
    main(args.model, args.base_url, args.api_key, args.n)
