"""
Experiment 8 - Question 10: Book Chapter Processor

Scenario: eBook chapters are stored as text files (chapter1.txt). Count how
many lines the chapter has and extract the first two lines as a teaser, saving
the teaser in chapter_teaser.txt.

Run: python q10_book_chapter_processor.py
"""

import os
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
INPUT_FILE = os.path.join(DATA, "chapter1.txt")
OUTPUT_FILE = os.path.join(DATA, "chapter_teaser.txt")

SAMPLE = """Chapter 1: The Ward at Midnight
The corridor lights of the district hospital never fully went out.
Dr. Kavita Rao walked the length of Ward C with a clipboard she no longer
needed, because the numbers she wanted were already on the screen in her
pocket.
Three years earlier, finding a free bed meant four phone calls and a guess.
The night nurse would shout across the corridor, someone would check a
register, and a patient on a trolley would wait.
Tonight the dashboard said eleven beds free in Ward C and two in the ICU,
and it had said so within thirty seconds of the last discharge.
She stopped at the nurses' station.
"Anything from the taluka hospital?" she asked.
"Two transfers," the nurse said, not looking up. "They checked availability
before dispatching. First time that has happened."
Kavita wrote nothing down.
The system had not cured anybody. It had only removed the waiting that came
from not knowing, which, she had come to believe, was its own kind of illness.
Outside, an ambulance turned in without its siren, which meant there was time.
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
        lines = fh.read().splitlines()

    text = "\n".join(lines)
    words = text.split()
    sentences = [s.strip() for s in text.replace("!", ".").replace("?", ".")
                 .split(".") if s.strip()]

    print(f"=== read {os.path.basename(INPUT_FILE)} ===")
    print(f"  lines in the chapter : {len(lines)}")
    print(f"  non-empty lines      : {sum(1 for ln in lines if ln.strip())}")
    print(f"  words                : {len(words)}")
    print(f"  characters           : {len(text)}")
    print(f"  sentences            : {len(sentences)}")
    print(f"  file size            : {os.path.getsize(INPUT_FILE)} bytes")

    first_two = lines[:2]
    print("\n=== teaser: the first two lines ===")
    for i, line in enumerate(first_two, 1):
        print(f"  {i}. {line}")

    print("\n=== reading metrics ===")
    print(f"  average words per sentence : {len(words) / len(sentences):.1f}")
    print(f"  average word length        : "
          f"{sum(len(w.strip('.,\"')) for w in words) / len(words):.2f} chars")
    print(f"  estimated reading time     : "
          f"{len(words) / 200:.1f} minute(s) at 200 wpm")

    print("\n=== dialogue lines ===")
    for n, line in enumerate(lines, 1):
        if '"' in line:
            print(f"  line {n:>2}: {line.strip()[:70]}")

    stop = {"the", "and", "that", "with", "which", "from", "what", "than",
            "they", "have", "been", "were", "would", "there", "because",
            "before", "only", "said", "came", "into", "without", "already"}
    freq = Counter(w.strip('.,"\'').lower() for w in words
                   if len(w) > 3 and w.strip('.,"\'').lower() not in stop)
    print("\n=== most frequent content words ===")
    for word, n in freq.most_common(8):
        print(f"  {word:<14}{n}")

    print("\n=== longest lines ===")
    for n, line in sorted(enumerate(lines, 1), key=lambda p: -len(p[1]))[:3]:
        print(f"  line {n:>2} ({len(line)} chars): {line[:60]}...")

    print("\n=== chapter title detected ===")
    print(f"  {lines[0] if lines[0].lower().startswith('chapter') else '(none)'}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as fh:
        for line in first_two:
            fh.write(line + "\n")

    print(f"\n=== wrote {OUTPUT_FILE} ===")
    with open(OUTPUT_FILE, "r", encoding="utf-8") as fh:
        teaser = fh.read()
    for i, line in enumerate(teaser.splitlines(), 1):
        print(f"  {i}. {line}")

    print(f"\n  teaser   : {len(teaser.split())} words, "
          f"{os.path.getsize(OUTPUT_FILE)} bytes")
    print(f"  chapter  : {len(words)} words, "
          f"{os.path.getsize(INPUT_FILE)} bytes")
    print(f"  the teaser is "
          f"{len(teaser.split()) / len(words) * 100:.1f}% of the chapter")
