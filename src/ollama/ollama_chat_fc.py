import argparse
import json
import requests
import time

# See
# - [Tool support](https://ollama.com/blog/tool-support)
# Models
# - [llama3.2](https://ollama.com/library/llama3.2)
OLLAMA_HOST = "localhost"
OLLAMA_PORT = 11434
MODEL_NAME = "llama3.2"


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


def main(host: str, port: int = OLLAMA_PORT, model: str = MODEL_NAME):
    available_functions = {"get_product_name_by_id": get_product_name_by_id}
    param_types = {"get_product_name_by_id": {"product_id": int}}
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

    messages = [
        {
            "role": "system",
            "content": "You are an assistant who prefers concise answers, typically one sentence.",
        },
        {
            "role": "user",
            "content": "Please tell me the product name that corresponds to product ID 33333.",
        },
    ]

    payload = {
        "model": model,
        "messages": messages,
        "tools": [tool_get_product_name_by_id],
        "stream": False,
        "temperature": 0.1,
    }
    print(f"Model: {model}")
    print("Messages:")
    for message in payload["messages"]:
        print(f"role: {message.get('role')}")
        print(message.get("content"))
        print()

    print(f"Request: {json.dumps(payload, indent=2)}")
    t_0 = time.time()
    response = requests.post(
        f"http://{host}:{port}/v1/chat/completions",
        headers={"Content-Type": "application/json"},
        json=payload,
        stream=False,
    )
    t_1 = time.time()
    time_delta = t_1 - t_0

    # See: https://github.com/ollama/ollama/blob/main/docs/api.md#chat-request-with-history-with-tools
    print(f"Response({time_delta:.1f}[s]):")
    res_json = response.json()
    print(json.dumps(res_json, indent=2))
    print("")
    for choice in res_json.get("choices", []):
        message = choice.get("message")
        # the tool call result appended to history
        messages.append(message)
        if "tool_calls" in message:
            for tool_call in message.get("tool_calls"):
                func = tool_call.get("function")
                func_name = func.get("name")
                arguments = json.loads(func.get("arguments"))
                if func_name == "get_product_name_by_id":
                    # Convert {"product_id": "1234"} to {"product_id": 1234}
                    expected_type = param_types[func_name]
                    converted_params = {
                        k: expected_type[k](v) if k in expected_type else v
                        for k, v in arguments.items()
                    }
                    # Call get_product_name_by_id(product_id=1234)
                    ret = available_functions[func_name](**converted_params)
                    messages.append(
                        {
                            "role": "tool",
                            "name": func_name,
                            "content": ret,
                            "tool_call_id": tool_call.get("id"),
                        }
                    )

    payload["messages"] = messages
    print()
    print(f"Request: {json.dumps(payload, indent=2)}")
    t_2 = time.time()
    response = requests.post(
        f"http://{host}:{port}/v1/chat/completions",
        headers={"Content-Type": "application/json"},
        json=payload,
        stream=False,
    )
    t_3 = time.time()
    time_delta = t_3 - t_2
    print(f"Response({time_delta:.1f}[s]):")
    res_json = response.json()
    print(json.dumps(res_json, indent=2))
    print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send a simple chat request to an Ollama server.")
    parser.add_argument(
        "-H",
        "--host",
        default=OLLAMA_HOST,
        help=(
            "Hostname (or host) of the Ollama server. "
            f"Port :{OLLAMA_PORT} will be used unless included in the host."
        ),
    )
    parser.add_argument(
        "-m", "--model", default=MODEL_NAME, help="Model name to use (default: %(default)s)."
    )
    args = parser.parse_args()
    main(args.host, OLLAMA_PORT, args.model)
