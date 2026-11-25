"""
Experiment 8 - Question 1: Log File Analysis

Scenario: A server generates a daily log file (server_log.txt). Read the log,
count the number of log entries (lines), extract the first two log messages
and write them into log_summary.txt for the system administrator.

Run: python q1_log_file_analysis.py
"""

import os
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
INPUT_FILE = os.path.join(DATA, "server_log.txt")
OUTPUT_FILE = os.path.join(DATA, "log_summary.txt")

SAMPLE = """2026-11-24 00:00:12 INFO  nginx started, listening on :443
2026-11-24 00:04:51 INFO  GET /api/beds 200 in 42ms
2026-11-24 00:17:03 WARN  slow query on appointments table, 1840ms
2026-11-24 01:02:44 INFO  GET /api/doctors 200 in 28ms
2026-11-24 01:33:19 ERROR failed to reach supabase: connection reset
2026-11-24 01:33:25 INFO  retry succeeded after 1 attempt
2026-11-24 02:15:08 INFO  nightly backup started
2026-11-24 02:41:55 INFO  nightly backup finished, 184 MB
2026-11-24 06:00:01 INFO  cron: appointment reminders dispatched
2026-11-24 09:12:37 ERROR 500 on POST /api/appointments, payload too large
2026-11-24 09:12:40 WARN  rate limit hit for 49.36.x.x
2026-11-24 14:48:22 INFO  GET /api/medications 200 in 31ms
"""


def ensure_sample():
    os.makedirs(DATA, exist_ok=True)
    if not os.path.exists(INPUT_FILE):
        with open(INPUT_FILE, "w", encoding="utf-8") as fh:
            fh.write(SAMPLE)
        print(f"[setup] created sample input {INPUT_FILE}")


if __name__ == "__main__":
    ensure_sample()

    # --- read the whole log, one line per entry ---
    with open(INPUT_FILE, "r", encoding="utf-8") as fh:
        lines = fh.readlines()

    entries = [ln.rstrip("\n") for ln in lines if ln.strip()]

    print(f"=== read {os.path.basename(INPUT_FILE)} ===")
    print(f"  total lines in the file : {len(lines)}")
    print(f"  non-empty log entries   : {len(entries)}")
    print(f"  file size               : {os.path.getsize(INPUT_FILE)} bytes")

    first_two = entries[:2]
    print("\n=== first two log messages ===")
    for i, entry in enumerate(first_two, 1):
        print(f"  {i}. {entry}")

    print("\n=== last entry, for context ===")
    print(f"  {entries[-1]}")

    # --- severity breakdown, useful for the admin ---
    levels = Counter()
    for entry in entries:
        parts = entry.split()
        if len(parts) >= 3:
            levels[parts[2]] += 1

    print("\n=== severity breakdown ===")
    for level, count in levels.most_common():
        print(f"  {level:<7}{count:>3}  ({count / len(entries) * 100:.1f}%)")

    errors = [e for e in entries if " ERROR " in e]
    warnings = [e for e in entries if " WARN " in e]

    print(f"\n=== {len(errors)} error(s) needing attention ===")
    for e in errors:
        print("  ", e)
    print(f"\n=== {len(warnings)} warning(s) ===")
    for w in warnings:
        print("  ", w)

    # --- write the summary file ---
    with open(OUTPUT_FILE, "w", encoding="utf-8") as fh:
        fh.write(first_two[0] + "\n")
        fh.write(first_two[1] + "\n")

    print(f"\n=== wrote {OUTPUT_FILE} ===")
    with open(OUTPUT_FILE, "r", encoding="utf-8") as fh:
        for line in fh:
            print("  " + line.rstrip())

    print(f"\n  summary file line count: "
          f"{sum(1 for _ in open(OUTPUT_FILE, encoding='utf-8'))}")

    print("\n=== admin one-line verdict ===")
    print(f"  {len(entries)} entries, {levels.get('ERROR', 0)} error(s), "
          f"{levels.get('WARN', 0)} warning(s) - " +
          ("investigate the errors" if errors else "log looks healthy"))
