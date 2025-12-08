import json
import requests
import argparse
import time


OLLAMA_HOST = "localhost"
OLLAMA_PORT = 11434
MODEL_NAME = "mistral"


def main(host: str, port: int = OLLAMA_PORT, model: str = MODEL_NAME):
    """
    Sends a request to the Ollama server and receives the response as a stream.

    Args:
        host (str): The hostname of the Ollama server.
        port (int): The port number of the Ollama server.
        model (str): The name of the model to use.
    """
    payload = {
        "model": model,
        "prompt": "What is the tallest mountain in the world?",
        "stream": True,
    }
    print(f"Model: {model}")
    print(f"Prompt: {payload['prompt']}")

    print("Response:")
    t_0 = time.time()
    try:
        response = requests.post(
            f"http://{host}:{port}/api/generate",
            headers={"Content-Type": "application/json"},
            json=payload,
            stream=True,
        )
        response.raise_for_status()

    except requests.exceptions.RequestException as e:
        print(f"ERROR: An error was detected in the HTTP request. : {e}")
        return

    for line in response.iter_lines():
        try:
            data = json.loads(line.decode("utf-8"))
            if data.get("done"):
                print("[done]")
                break
            print(data.get("response", ""), end="", flush=True)

        except json.JSONDecodeError as e:
            print(f"ERROR: JSON decode error : MESSAGE={e}")

    t_1 = time.time()
    time_delta = t_1 - t_0
    print("")
    print(f"dt = {time_delta:.1f}[s]")


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
