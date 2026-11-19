import json
from pathlib import Path

# 1. Find the log file next to this script
log_file = Path(__file__).parent / "log.jsonl"

# 2. Read every line into a list of dicts
records = []
for line in open(log_file, "r", encoding="utf-8"):
    record = json.loads(line)
    records.append(record)

# 3. Calculate the stats

runs = len(records)
total_latency = sum(r["latency_s"] for r in records)

# TODO: average latency = total divided by number of runs
average_latency = total_latency / runs if runs > 0 else 0

slowest = max(records, key=lambda r: r["latency_s"])
# TODO: total tokens out (hint: same pattern as total_latency)
total_tokens_out = sum(r["tokens_out"] for r in records)

# 4. Print the report
print(f"Runs: {runs}")

# TODO: print average latency with 2 decimals, e.g. "Average latency: 2.13s"
print(f"Average latency: {average_latency:.2f}s")

print(f'Slowest: {slowest["latency_s"]}s ("{slowest["question"]}")')
print(f"Total tokens out: {total_tokens_out}")