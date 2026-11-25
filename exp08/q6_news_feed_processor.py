"""
Experiment 8 - Question 6: News Feed Processor

Scenario: news_feed.txt contains headlines fetched from a news API. Count how
many headlines were fetched, extract the first two and save them to
top_stories.txt.

Run: python q6_news_feed_processor.py
"""

import os
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
INPUT_FILE = os.path.join(DATA, "news_feed.txt")
OUTPUT_FILE = os.path.join(DATA, "top_stories.txt")

SAMPLE = """HEALTH|State expands free dialysis scheme to 40 more district hospitals
TECH|Open-source hospital information system crosses 500 deployments
HEALTH|Monsoon dengue cases drop 18 percent after ward-level surveillance
POLICY|Draft rules would require bed-availability dashboards at every district hospital
TECH|Researchers release an anonymised bed-occupancy dataset covering 14 months
EDUCATION|Engineering syllabus adds a mandatory data-handling lab from next term
HEALTH|Vaccine cold-chain audit flags 12 percent of rural units
TECH|Low-cost IoT temperature logger passes field trial in two districts
POLICY|Health ministry proposes a single appointment booking standard
EDUCATION|Two universities open joint health-informatics programme
HEALTH|Blood bank network goes live across six cities
TECH|Hospital chatbot pilot reduces front-desk queue times by a third
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
        raw = [ln.rstrip("\n") for ln in fh if ln.strip()]

    print(f"=== read {os.path.basename(INPUT_FILE)} ===")
    print(f"  headlines fetched : {len(raw)}")
    print(f"  file size         : {os.path.getsize(INPUT_FILE)} bytes")

    items = []
    for line in raw:
        section, _, headline = line.partition("|")
        items.append((section.strip(), headline.strip() or section.strip()))

    first_two = raw[:2]
    print("\n=== first two headlines ===")
    for i, line in enumerate(first_two, 1):
        section, _, headline = line.partition("|")
        print(f"  {i}. [{section}] {headline}")

    print("\n=== all headlines by section ===")
    sections = Counter(s for s, _ in items)
    for section, count in sections.most_common():
        print(f"\n  {section} ({count})")
        for s, headline in items:
            if s == section:
                print(f"    - {headline}")

    print("\n=== section share ===")
    for section, count in sections.most_common():
        share = count / len(items) * 100
        print(f"  {section:<11}{count:>3}  {share:>5.1f}%  {'#' * count}")

    lengths = [len(h) for _, h in items]
    print("\n=== headline length ===")
    print(f"  shortest : {min(lengths)} chars - "
          f"{min((h for _, h in items), key=len)}")
    print(f"  longest  : {max(lengths)} chars - "
          f"{max((h for _, h in items), key=len)}")
    print(f"  average  : {sum(lengths) / len(lengths):.1f} chars")

    words = Counter()
    stop = {"the", "and", "for", "with", "from", "that", "would", "after",
            "every", "more", "two", "its"}
    for _, h in items:
        words.update(w.strip(".,").lower() for w in h.split()
                     if len(w) > 3 and w.lower() not in stop)
    print("\n=== trending terms ===")
    for word, count in words.most_common(8):
        print(f"  {word:<16}{count}")

    print("\n=== headlines mentioning 'hospital' ===")
    for s, h in items:
        if "hospital" in h.lower():
            print(f"  [{s}] {h}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as fh:
        for line in first_two:
            _, _, headline = line.partition("|")
            fh.write(headline.strip() + "\n")

    print(f"\n=== wrote {OUTPUT_FILE} ===")
    with open(OUTPUT_FILE, "r", encoding="utf-8") as fh:
        for i, line in enumerate(fh, 1):
            print(f"  {i}. {line.rstrip()}")

    print(f"\n  top_stories.txt holds "
          f"{sum(1 for _ in open(OUTPUT_FILE, encoding='utf-8'))} headline(s) "
          f"out of {len(raw)} fetched")
