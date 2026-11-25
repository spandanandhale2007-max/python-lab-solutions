"""
Experiment 8 - Question 9: Survey Responses Handler

Scenario: survey_responses.txt contains responses to a survey question. Count
how many people responded and extract the first two responses into
sample_responses.txt.

Run: python q9_survey_responses_handler.py
"""

import os
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
INPUT_FILE = os.path.join(DATA, "survey_responses.txt")
OUTPUT_FILE = os.path.join(DATA, "sample_responses.txt")

QUESTION = ("How likely are you to recommend the MediVerse bed-availability "
            "feature? (0-10, plus a comment)")

SAMPLE = """9 | Finding a free ICU bed used to take four phone calls. Now it is one screen.
8 | Useful, but the data looked stale once during the evening rush.
10 | Exactly what a district hospital needs. Shared it with two colleagues.
6 | Works, though the mobile layout squeezes the ward names.
7 | Good. Please add a filter for paediatric beds.
3 | It showed a bed as free that was already taken. Lost trust after that.
9 | The refresh is fast and the colour coding is clear.
10 | Our front desk now answers bed queries without calling the wards.
5 | Fine for one hospital, but we need a multi-hospital view.
8 | Solid. An SMS alert when ICU capacity drops below 10% would help.
2 | Could not log in for two days last week.
9 | Clean interface, no training needed for the staff.
7 | Decent, add a printable daily occupancy report.
10 | Best improvement to our workflow this year.
"""


def ensure_sample():
    os.makedirs(DATA, exist_ok=True)
    if not os.path.exists(INPUT_FILE):
        with open(INPUT_FILE, "w", encoding="utf-8") as fh:
            fh.write(SAMPLE)
        print(f"[setup] created sample input {INPUT_FILE}")


def nps_bucket(score):
    if score >= 9:
        return "promoter"
    if score >= 7:
        return "passive"
    return "detractor"


if __name__ == "__main__":
    ensure_sample()

    with open(INPUT_FILE, "r", encoding="utf-8") as fh:
        lines = [ln.rstrip("\n") for ln in fh if ln.strip()]

    print(f"=== survey question ===")
    print(f"  {QUESTION}")
    print(f"\n=== read {os.path.basename(INPUT_FILE)} ===")
    print(f"  people responded : {len(lines)}")
    print(f"  file size        : {os.path.getsize(INPUT_FILE)} bytes")

    responses = []
    for line in lines:
        score_text, _, comment = line.partition("|")
        try:
            responses.append((int(score_text.strip()), comment.strip()))
        except ValueError:
            responses.append((None, line.strip()))

    first_two = lines[:2]
    print("\n=== first two responses ===")
    for i, line in enumerate(first_two, 1):
        print(f"  {i}. {line}")

    scored = [(s, c) for s, c in responses if s is not None]
    scores = [s for s, _ in scored]

    print("\n=== score distribution ===")
    counts = Counter(scores)
    for score in range(11):
        n = counts.get(score, 0)
        if n:
            print(f"  {score:>2} : {'#' * n} ({n})")

    print("\n=== statistics ===")
    print(f"  responses with a score : {len(scored)}")
    print(f"  average score          : {sum(scores) / len(scores):.2f}")
    print(f"  highest / lowest       : {max(scores)} / {min(scores)}")
    srt = sorted(scores)
    mid = len(srt) // 2
    median = srt[mid] if len(srt) % 2 else (srt[mid - 1] + srt[mid]) / 2
    print(f"  median                 : {median}")

    buckets = Counter(nps_bucket(s) for s in scores)
    promoters = buckets.get("promoter", 0)
    detractors = buckets.get("detractor", 0)
    nps = (promoters - detractors) / len(scores) * 100

    print("\n=== net promoter breakdown ===")
    for name in ("promoter", "passive", "detractor"):
        n = buckets.get(name, 0)
        print(f"  {name:<11}{n:>3}  {n / len(scores) * 100:>5.1f}%")
    print(f"  NPS : {nps:+.1f}")

    print("\n=== detractor comments (act on these first) ===")
    for s, c in scored:
        if nps_bucket(s) == "detractor":
            print(f"  [{s}] {c}")

    print("\n=== feature requests mentioned ===")
    for s, c in scored:
        low = c.lower()
        if any(w in low for w in ("add", "please", "need", "would help")):
            print(f"  [{s}] {c}")

    words = Counter()
    for _, c in scored:
        words.update(w.strip(".,").lower() for w in c.split() if len(w) > 4)
    print("\n=== most mentioned terms ===")
    for word, n in words.most_common(6):
        print(f"  {word:<14}{n}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as fh:
        for line in first_two:
            fh.write(line + "\n")

    print(f"\n=== wrote {OUTPUT_FILE} ===")
    with open(OUTPUT_FILE, "r", encoding="utf-8") as fh:
        for i, line in enumerate(fh, 1):
            print(f"  {i}. {line.rstrip()}")
    print(f"\n  sample file: "
          f"{sum(1 for _ in open(OUTPUT_FILE, encoding='utf-8'))} of "
          f"{len(lines)} responses")
