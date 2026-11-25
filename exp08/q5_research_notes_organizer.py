"""
Experiment 8 - Question 5: Research Notes Organizer

Scenario: A research assistant adds daily notes to research_notes.txt.
Summarise the total number of notes, extract the first two entries and save
them into note_summary.txt.

Run: python q5_research_notes_organizer.py
"""

import os
import re
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
INPUT_FILE = os.path.join(DATA, "research_notes.txt")
OUTPUT_FILE = os.path.join(DATA, "note_summary.txt")

DATE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})")
TAG_RE = re.compile(r"#(\w+)")

SAMPLE = """2026-11-10 #literature Read Kumar et al. on hospital bed allocation; queueing model, not ML.
2026-11-11 #dataset Found the open AIIMS bed occupancy dataset, 14 months, hourly granularity.
2026-11-12 #method Tried a simple moving average baseline; MAE 4.2 beds, surprisingly hard to beat.
2026-11-13 #literature Chen 2024 argues occupancy is seasonal at the week level, matches our data.
2026-11-14 #method Added day-of-week features; MAE drops to 3.1 beds.
2026-11-17 #dataset Cleaned 312 duplicate rows caused by the double-logging bug.
2026-11-18 #meeting Coordinator wants a demo with real screenshots by 30 November.
2026-11-19 #method Tried gradient boosting; MAE 2.6 but the model is hard to explain in a viva.
2026-11-20 #writing Drafted the methodology section, 900 words.
2026-11-21 #todo Need an ablation table and one clear figure of weekly seasonality.
2026-11-24 #writing Rewrote the introduction after feedback; tightened the problem statement.
"""


def ensure_sample():
    os.makedirs(DATA, exist_ok=True)
    if not os.path.exists(INPUT_FILE):
        with open(INPUT_FILE, "w", encoding="utf-8") as fh:
            fh.write(SAMPLE)
        print(f"[setup] created sample input {INPUT_FILE}")


if __name__ == "__main__":
    ensure_sample()

    with open(INPUT_FILE, "r", encoding="utf-8") as fh:
        notes = [ln.rstrip("\n") for ln in fh if ln.strip()]

    print(f"=== read {os.path.basename(INPUT_FILE)} ===")
    print(f"  total notes : {len(notes)}")
    print(f"  file size   : {os.path.getsize(INPUT_FILE)} bytes")
    words = sum(len(n.split()) for n in notes)
    print(f"  total words : {words}")
    print(f"  average note: {words / len(notes):.1f} words")

    first_two = notes[:2]
    print("\n=== first two entries ===")
    for i, n in enumerate(first_two, 1):
        print(f"  {i}. {n}")

    dates = [DATE_RE.match(n).group(1) for n in notes if DATE_RE.match(n)]
    print("\n=== date coverage ===")
    print(f"  first entry : {dates[0]}")
    print(f"  last entry  : {dates[-1]}")
    print(f"  distinct days with notes : {len(set(dates))}")
    busiest = Counter(dates).most_common(1)[0]
    print(f"  busiest day : {busiest[0]} with {busiest[1]} note(s)")

    tags = Counter()
    for n in notes:
        tags.update(TAG_RE.findall(n))
    print("\n=== notes by tag ===")
    for tag, count in tags.most_common():
        print(f"  #{tag:<14}{count:>3}  {'#' * count}")

    print("\n=== notes grouped by tag ===")
    for tag, _ in tags.most_common():
        print(f"\n  #{tag}")
        for n in notes:
            if tag in TAG_RE.findall(n):
                print(f"    {n[:78]}")

    todos = [n for n in notes if "#todo" in n]
    print(f"\n=== open action items ({len(todos)}) ===")
    for t in todos:
        print("  ", t)
    if not todos:
        print("  none")

    print("\n=== progress on the stated metric ===")
    for n in notes:
        m = re.search(r"MAE ([\d.]+)", n)
        if m:
            print(f"  {DATE_RE.match(n).group(1)}  MAE {m.group(1)} beds")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as fh:
        fh.write(f"Total notes: {len(notes)}\n")
        fh.write(f"Period: {dates[0]} to {dates[-1]}\n")
        fh.write("First two entries:\n")
        for n in first_two:
            fh.write(n + "\n")

    print(f"\n=== wrote {OUTPUT_FILE} ===")
    with open(OUTPUT_FILE, "r", encoding="utf-8") as fh:
        for line in fh:
            print("  " + line.rstrip())
    print(f"\n  summary file: "
          f"{sum(1 for _ in open(OUTPUT_FILE, encoding='utf-8'))} line(s)")
