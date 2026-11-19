import json
from pathlib import Path

log_file = Path(__file__).parent / "log.jsonl"

records = []
for line in open(log_file, encoding="utf-8"):
    records.append(json.loads(line))

if not records:
    print("No records found.")
    exit()

ok = [r for r in records if r.get("status", "ok") == "ok"]
errors = [r for r in records if r.get("status") == "error"]

runs = len(records)
error_rate = len(errors) / runs * 100

print(f"Runs: {runs} (ok: {len(ok)}, errors: {len(errors)})")
print(f"Error rate: {error_rate:.1f}%")

if ok:
    avg = sum(r["latency_s"] for r in ok) / len(ok)
    slowest = max(ok, key=lambda r: r["latency_s"])
    tokens = sum(r["tokens_out"] or 0 for r in ok)
    print(f"Average latency (ok runs): {avg:.2f}s")
    print(f'Slowest: {slowest["latency_s"]}s ("{slowest["question"]}")')
    print(f"Total tokens out: {tokens}")

for r in errors:
    print(f'  ERROR: {r["error"]}  ("{r["question"]}")')