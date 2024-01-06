"""Request with body"""
import json

import requests


def main():
    """Sending request with JSON data as a payload and headers."""
    req_url = "https://httpbin.org/post"
    rsp = requests.post(
        req_url,
        json={"id": 1001, "name": "Apple", "price": 300},
        headers={"Content-Type": "application/json; charset=utf-8"},
    )
    print(f"{rsp.status_code} url={rsp.url}")
    print("Headers:")
    print("\n".join([f"  {k}: {v}" for k, v in rsp.headers.items()]))

    print("Body:")
    if "application/json" in rsp.headers["content-type"]:
        print(json.dumps(rsp.json(), indent=2))
    else:
        print(rsp.text)


if __name__ == "__main__":
    main()

# EOF
