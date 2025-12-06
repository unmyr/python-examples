import json
import requests
import argparse
import time


OLLAMA_HOST = "localhost"
OLLAMA_PORT = 11434
MODEL_NAME = "mistral"


def main(host: str, port: int = OLLAMA_PORT, model: str = MODEL_NAME):
    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "You are an assistant who prefers concise answers, typically one sentence.",
            },
            {"role": "user", "content": "What is the tallest mountain in the world?"},
        ],
    }
    t_0 = time.time()
    response = requests.post(
        f"http://{host}:{port}/api/chat",
        headers={"Content-Type": "application/json"},
        json=payload,
        stream=True,
    )
    for line in response.iter_lines():
        if line:
            data = json.loads(line)
            print(data.get("message", {}).get("content", ""), end="")
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
