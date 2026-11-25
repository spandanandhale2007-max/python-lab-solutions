"""
Experiment 7 - Question 2: Newsletter Subscription Validator

Scenario: A website collects emails for a newsletter. The raw submissions are
stored in submissions.txt, which includes noise text. Use regex to extract
only the valid email addresses for building the subscriber list.

Run: python q2_newsletter_validator.py
"""

import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
INPUT_FILE = os.path.join(DATA, "submissions.txt")
OUTPUT_FILE = os.path.join(DATA, "subscriber_list.txt")
REJECT_FILE = os.path.join(DATA, "rejected_submissions.txt")

# A stricter pattern than a plain search: anchored per candidate token.
STRICT_RE = re.compile(
    r"^[A-Za-z0-9](?:[A-Za-z0-9._%+\-]*[A-Za-z0-9])?"      # local part
    r"@"
    r"(?:[A-Za-z0-9](?:[A-Za-z0-9\-]*[A-Za-z0-9])?\.)+"    # domain labels
    r"[A-Za-z]{2,}$"                                        # TLD
)
CANDIDATE_RE = re.compile(r"\S+@\S+")

SAMPLE = """subscribe me please -> spandan.andhale@example.com
yes!! riya93@mitwpu.edu.in
i want the weekly digest: aman_k99@sub.domain.co.in
not.an.email.at.all
@nolocalpart.com
missing-domain@
double@@at.com
user@nodot
trailing.dot@domain.
.leading.dot@domain.com
spaces in name@domain.com
too@short.c
UPPER.CASE@EXAMPLE.COM
spandan.andhale@example.com (already above, duplicate)
neha+newsletter@gmail.com
sana.shaikh@zoho.in
omkar..patil@example.com
hello_world-123@my-domain.org
admin@localhost
feedback@company.co.uk
<p>html noise</p> contact us at support@mediverse.in </p>
tel: 020-2555-1234
"""


def ensure_sample():
    os.makedirs(DATA, exist_ok=True)
    if not os.path.exists(INPUT_FILE):
        with open(INPUT_FILE, "w", encoding="utf-8") as fh:
            fh.write(SAMPLE)
        print(f"[setup] created sample input {INPUT_FILE}")


def reason(candidate):
    e = candidate.strip().strip("<>()[],;:\"'")
    if e.count("@") == 0:
        return "no @ sign"
    if e.count("@") > 1:
        return "multiple @ signs"
    local, _, domain = e.partition("@")
    if not local:
        return "empty local part"
    if not domain:
        return "empty domain"
    if ".." in e:
        return "consecutive dots"
    if local.startswith(".") or local.endswith("."):
        return "local part starts or ends with a dot"
    if "." not in domain:
        return "domain has no dot (no TLD)"
    if domain.endswith("."):
        return "domain ends with a dot"
    if len(domain.rsplit(".", 1)[1]) < 2:
        return "top level domain too short"
    return "fails the strict pattern"


if __name__ == "__main__":
    ensure_sample()

    with open(INPUT_FILE, "r", encoding="utf-8") as fh:
        lines = fh.read().splitlines()

    print(f"=== {len(lines)} raw submission line(s) read ===")

    valid, rejected = [], []
    for n, line in enumerate(lines, 1):
        found = False
        for candidate in CANDIDATE_RE.findall(line):
            cleaned = candidate.strip().strip("<>()[],;:\"'")
            if STRICT_RE.match(cleaned):
                valid.append((n, cleaned.lower()))
                found = True
            else:
                rejected.append((n, candidate, reason(candidate)))
                found = True
        if not found and line.strip():
            rejected.append((n, line.strip(), "contains no @ candidate at all"))

    print(f"\n=== {len(valid)} valid address(es) ===")
    for n, e in valid:
        print(f"  line {n:>2}: {e}")

    print(f"\n=== {len(rejected)} rejection(s) with the reason ===")
    for n, raw, why in rejected:
        print(f"  line {n:>2}: {raw[:38]:<40} -> {why}")

    subscribers = []
    for _, e in valid:
        if e not in subscribers:
            subscribers.append(e)
    dupes = len(valid) - len(subscribers)

    print(f"\n=== final subscriber list: {len(subscribers)} address(es) ===")
    for i, e in enumerate(subscribers, 1):
        print(f"  {i:>2}. {e}")
    print(f"  duplicates removed: {dupes}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as fh:
        fh.write("\n".join(subscribers) + "\n")
    with open(REJECT_FILE, "w", encoding="utf-8") as fh:
        for n, raw, why in rejected:
            fh.write(f"line {n}\t{raw}\t{why}\n")

    print(f"\n  subscribers written to : {OUTPUT_FILE}")
    print(f"  rejections written to  : {REJECT_FILE}")

    print("\n=== why the loose pattern is not enough ===")
    loose = re.compile(r"[^\s]+@[^\s]+")
    loose_hits = loose.findall("\n".join(lines))
    print(f"  loose  '[^\\s]+@[^\\s]+'   matched {len(loose_hits)} token(s)")
    print(f"  strict anchored pattern  accepted {len(valid)} token(s)")
    print(f"  the strict pattern threw out "
          f"{len(loose_hits) - len(valid)} malformed entries")

    print("\n=== domain breakdown of the subscriber list ===")
    counts = {}
    for e in subscribers:
        d = e.split("@")[1]
        counts[d] = counts.get(d, 0) + 1
    for d, c in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])):
        print(f"  {d:<22} {c}")
