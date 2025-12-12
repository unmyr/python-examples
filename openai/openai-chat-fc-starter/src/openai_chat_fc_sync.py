import argparse
import json
import os
import random
import time

from openai import OpenAI


def get_product_name_by_id(product_id: int):
    """Get product name by id"""
    product_names = [
        "apple",
        "banana",
        "grape",
        "kiwi",
        "mango",
        "orange",
        "peach",
        "pineapple",
        "strawberry",
        "watermelon",
    ]
    i = product_id % len(product_names)
    return product_names[i]


def main(model: str, base_url: str, api_key: str):
    available_functions = {"get_product_name_by_id": get_product_name_by_id}
    param_types = {"get_product_name_by_id": {"product_id": int}}

    client = OpenAI(base_url=base_url, api_key=api_key)
    tool_get_product_name_by_id = {
        "type": "function",
        "function": {
            "name": "get_product_name_by_id",
            "description": "Returns the product name by product id",
            "parameters": {
                "type": "object",
                "properties": {"product_id": {"type": "integer", "description": "product id"}},
                "required": ["product_id"],
            },
        },
    }
    input_list = [
        {
            "role": "system",
            "content": "You are an assistant who prefers concise answers, typically one sentence.",
        },
        {
            "role": "user",
            "content": (
                "Please tell me the product name that corresponds to product ID"
                f" {random.randint(0, 9)}."
            ),
        },
    ]
    print(f"Model: {model}")
    stop = False
    for r_i in [1, 2, 3]:
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
            tools=[tool_get_product_name_by_id],
            stream=False,
        )
        t_1 = time.time()
        time_delta = t_1 - t_0
        print(f"Response({time_delta:.1f}[s]): id={chat_completion.id}")
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
                stop = True
                print(choice.message.content)

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
                            output = available_functions[f_name](**f_arguments_converted)
                            input_list.append(
                                {
                                    "role": "tool",
                                    "tool_call_id": tool_call.id,
                                    "name": f_name,
                                    "content": json.dumps({"product_name": output}),
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
