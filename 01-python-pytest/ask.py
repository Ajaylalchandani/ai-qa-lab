import httpx
import sys
import json
import time
from datetime import datetime, timezone
from pathlib import Path




if len(sys.argv) < 2:
    print("Usage: python ask.py <question>")
    sys.exit(1)
question = " ".join(sys.argv[1:])



url = "http://localhost:11434/api/generate"
model = "llama3.2"


payload = {
    "model": model,
    "prompt": question,
    "stream": False,
}

start =time.perf_counter()
response = httpx.post(url, json=payload, timeout=60)
elapsed = time.perf_counter() - start
response.raise_for_status()
data = response.json()
answer = data["response"]

# NEW: build one log record

record = {
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "model": model,
    "question": question,
    "answer": answer,
    "tokens_in": data["prompt_eval_count"],
    "tokens_out": data["eval_count"],
    "latency_s": round(elapsed, 2),
}
# NEW: append it as one line to log.jsonl, next to this script
log_file = Path(__file__).parent / "log.jsonl"

with open(log_file, "a", encoding="utf-8") as f:
    f.write(json.dumps(record) + "\n")

print(answer)

print(f"Tokens in: {record['tokens_in']}, out: {record['tokens_out']}, latency: {elapsed:.2f}s")
# print(data["response"])
# print(f"Tokens in: {data['prompt_eval_count']}, tokens out: {data['eval_count']}")
