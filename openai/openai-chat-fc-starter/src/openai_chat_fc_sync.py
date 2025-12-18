import argparse
import json
import os
import random
import time
import types

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


def get_product_price_by_id(product_id: int):
    """
    Get price by product id

    :param product_id: Description
    :type product_id: int
    """
    prices: types.Dict[int:str] = {
        0: "70 yen",
        1: "30 yen",
        2: "60 yen",
        3: "140 yen",
        4: "250 yen",
        5: "60 yen",
        6: "50 yen",
        7: "80 yen",
        8: "150 yen",
        9: "90 yen",
    }
    return prices.get(product_id, None)


def main(model: str, base_url: str, api_key: str):
    available_functions = {
        "get_product_name_by_id": get_product_name_by_id,
        "get_product_price_by_id": get_product_price_by_id,
    }
    param_types = {
        "get_product_name_by_id": {"product_id": int},
        "get_product_price_by_id": {"product_id": int},
    }

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

    tool_get_product_price_by_id = {
        "type": "function",
        "function": {
            "name": "get_product_price_by_id",
            "description": "Returns the price in yen of a product by product ID",
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
                "Please tell me the product name and price that corresponds to product ID"
                f" {random.randint(0, 9)}."
            ),
        },
    ]
    print(f"Model: {model}")
    client = OpenAI(base_url=base_url, api_key=api_key)

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
            tools=[tool_get_product_name_by_id, tool_get_product_price_by_id],
            stream=False,
        )
        t_1 = time.time()
        elapsed_time = t_1 - t_0
        tps = chat_completion.usage.completion_tokens / elapsed_time
        print(f"Response({elapsed_time:.1f}[s], {tps:.2f} [token/s]): id={chat_completion.id}")
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
                tool_callers = []

                # Append tool_call requests to input_list
                for _, tool_call in enumerate(choice.message.tool_calls):
                    # print(f"tool_call={tool_call}")

                    # Fix LLM response type mismatch
                    # Lightweight LLM tends to ignore parameter types and pass them as strings,
                    # and doesn't understand type errors, so we have no choice but to convert
                    # the type in the Python application to match LLM.
                    f_name = tool_call.function.name
                    f_arguments = json.loads(tool_call.function.arguments)
                    expected_type = param_types[f_name]
                    f_arguments_converted = {
                        k: expected_type[k](v) if k in expected_type else v
                        for k, v in f_arguments.items()
                    }
                    print(
                        f"arguments={f_arguments}"
                        f" → arguments_converted={f_arguments_converted}"
                    )
                    tool_callers.append(
                        {
                            "index": tool_call.index,
                            "type": tool_call.type,
                            "id": tool_call.id,
                            "function": {
                                "name": f_name,
                                "arguments": json.dumps(f_arguments_converted),
                            },
                        }
                    )

                print(f"tool_caller={json.dumps(tool_callers, indent=2)}")
                input_list.append(
                    {
                        "role": choice.message.role,
                        "content": choice.message.content,
                        "tool_calls": tool_callers,
                    }
                )

                for tool_caller in tool_callers:
                    f_name = tool_caller.get('function').get('name')
                    if f_name not in available_functions:
                        print(f"ERROR: Function not found. : NAME={f_name}")
                        continue

                    try:
                        f_arguments = json.loads(tool_caller.get('function').get('arguments'))
                        output = available_functions[f_name](**f_arguments)
                        tool_response = {"product_name": output}

                    except TypeError as exc:
                        print(str(exc))
                        tool_response = {"error": str(exc)}

                    input_list.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_caller.get("id"),
                            "name": f_name,
                            "content": json.dumps(tool_response),
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
