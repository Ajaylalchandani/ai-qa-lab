import httpx
import sys
import os
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
PROVIDER = os.getenv("PROVIDER", "ollama")
TIMEOUT_S = 120

def write_log(record):
    log_file = Path(__file__).parent / "log.jsonl"
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")

def fail(message):
    elapsed = time.perf_counter() - start
    write_log({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "provider": PROVIDER,
        "question": question,
        "status": "error",  
        "error": message,
        "latency_s": round(elapsed, 2),
    })
    print(message)
    sys.exit(2)
    


def ask_ollama(question):
    model = "llama3.2"
    payload = {"model": model, "prompt": question, "stream": False}
    r = httpx.post("http://localhost:11434/api/generate", json=payload, timeout=TIMEOUT_S)
    r.raise_for_status()
    data = r.json()
    return model, data["response"], data["prompt_eval_count"], data["eval_count"]


def ask_gemini(question):
    model = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    headers = {"x-goog-api-key": os.environ["GEMINI_API_KEY"]}
    body = {"contents": [{"parts": [{"text": question}]}]}
    r = httpx.post(url, headers=headers, json=body, timeout=TIMEOUT_S)
    r.raise_for_status()
    data = r.json()
    answer = data["candidates"][0]["content"]["parts"][0]["text"]
    usage = data.get("usageMetadata", {})
    return model, answer, usage.get("promptTokenCount"), usage.get("candidatesTokenCount")


if len(sys.argv) < 2:
    print("Usage: python ask.py <question>")
    sys.exit(1)
question = " ".join(sys.argv[1:])

ask = ask_gemini if PROVIDER == "gemini" else ask_ollama

start = time.perf_counter()
try:
    model, answer, tokens_in, tokens_out = ask(question)    
except httpx.ConnectError:
    fail("Cannot reach Ollama at localhost:11434. Is it running?")

except KeyError as e:
    fail(f"Missing setting {e}: add it to your .env file")

except httpx.HTTPStatusError as e:
    fail(f"HTTP {e.response.status_code} from {PROVIDER}")

except httpx.ConnectTimeout:
    fail(f"Request timed out after {TIMEOUT_S} seconds.")


elapsed = time.perf_counter() - start

record = {
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "provider": PROVIDER,
    "model": model,
    "question": question,
    "answer": answer,
    "tokens_in": tokens_in,
    "tokens_out": tokens_out,
    "latency_s": round(elapsed, 2),
    "status": "ok",
}

write_log(record)


print(answer)
print(f"[{PROVIDER}/{model}] tokens in: {tokens_in}, out: {tokens_out}, latency: {elapsed:.2f}s")