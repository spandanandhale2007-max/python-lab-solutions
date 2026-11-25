"""
Experiment 8 - Question 2: Student Feedback Collection

Scenario: Feedback from students arrives in feedback.txt. Read the file, count
the total number of feedback entries and extract the first two responses. Save
the extracted feedback in sample_feedback.txt.

Run: python q2_student_feedback.py
"""

import os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
INPUT_FILE = os.path.join(DATA, "feedback.txt")
OUTPUT_FILE = os.path.join(DATA, "sample_feedback.txt")

POSITIVE = ["good", "great", "excellent", "helpful", "clear", "loved",
            "useful", "enjoyed", "best"]
NEGATIVE = ["slow", "boring", "confusing", "difficult", "poor", "rushed",
            "unclear", "too fast"]

SAMPLE = """The Python lab sessions were excellent, the examples were very clear.
Lectures move too fast for a first-year subject, please slow down.
Loved the hospital management case study, it made OOP concepts click.
The assignment deadlines overlap with other subjects, that is difficult.
Good use of real datasets in the pandas unit, very useful.
The projector in Lab 4 keeps failing, it wastes the first ten minutes.
More practice questions on dynamic programming would be helpful.
Teaching is great but the textbook is confusing in places.
The viva format is fair and the feedback afterwards is clear.
Please upload the slides before class, not after.
"""


def ensure_sample():
    os.makedirs(DATA, exist_ok=True)
    if not os.path.exists(INPUT_FILE):
        with open(INPUT_FILE, "w", encoding="utf-8") as fh:
            fh.write(SAMPLE)
        print(f"[setup] created sample input {INPUT_FILE}")


def sentiment(text):
    low = text.lower()
    pos = sum(1 for w in POSITIVE if w in low)
    neg = sum(1 for w in NEGATIVE if w in low)
    if pos > neg:
        return "positive"
    if neg > pos:
        return "negative"
    return "neutral"


if __name__ == "__main__":
    ensure_sample()

    with open(INPUT_FILE, "r", encoding="utf-8") as fh:
        responses = [ln.strip() for ln in fh if ln.strip()]

    print(f"=== read {os.path.basename(INPUT_FILE)} ===")
    print(f"  total feedback entries : {len(responses)}")
    print(f"  file size              : {os.path.getsize(INPUT_FILE)} bytes")
    words = sum(len(r.split()) for r in responses)
    print(f"  total words            : {words}")
    print(f"  average response length: {words / len(responses):.1f} words")

    first_two = responses[:2]
    print("\n=== first two responses ===")
    for i, r in enumerate(first_two, 1):
        print(f"  {i}. {r}")

    print("\n=== all responses with a sentiment tag ===")
    for i, r in enumerate(responses, 1):
        print(f"  {i:>2}. [{sentiment(r):<8}] {r}")

    counts = {}
    for r in responses:
        tag = sentiment(r)
        counts[tag] = counts.get(tag, 0) + 1

    print("\n=== sentiment summary ===")
    for tag in ("positive", "neutral", "negative"):
        n = counts.get(tag, 0)
        bar = "#" * n
        print(f"  {tag:<9}{n:>3}  |{bar}")
    print(f"  satisfaction: "
          f"{counts.get('positive', 0) / len(responses) * 100:.1f}% positive")

    print("\n=== longest and shortest response ===")
    print(f"  longest  ({len(max(responses, key=len))} chars): "
          f"{max(responses, key=len)}")
    print(f"  shortest ({len(min(responses, key=len))} chars): "
          f"{min(responses, key=len)}")

    print("\n=== action items (negative feedback) ===")
    actions = [r for r in responses if sentiment(r) == "negative"]
    for i, r in enumerate(actions, 1):
        print(f"  {i}. {r}")
    if not actions:
        print("  none")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as fh:
        for r in first_two:
            fh.write(r + "\n")

    print(f"\n=== wrote {OUTPUT_FILE} ===")
    with open(OUTPUT_FILE, "r", encoding="utf-8") as fh:
        content = fh.read()
    print(content.rstrip().replace("\n", "\n  ").rjust(0))
    print(f"\n  lines written : {len(content.splitlines())}")
    print(f"  bytes written : {len(content.encode())}")
