import httpx
import sys


if len(sys.argv) < 2:
    print("Usage: python ask.py <question>")
    sys.exit(1)
question = " ".join(sys.argv[1:])



url = "http://localhost:11434/api/generate"

payload = {
    "model": "llama3.2",
    "prompt": question,
    "stream": False,
}

response = httpx.post(url, json=payload, timeout=60)
response.raise_for_status()
data = response.json()

print(data["response"])
print(f"Tokens in: {data['prompt_eval_count']}, tokens out: {data['eval_count']}")
