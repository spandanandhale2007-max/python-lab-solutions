"""
Experiment 7 - Question 5: Social Media Profile Extractor

Scenario: Public social media profile text may contain email addresses hidden
inside the content. Use regex to extract any found emails and write them to
extracted_emails.txt.

Run: python q5_social_profile_extractor.py
"""

import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
INPUT_FILE = os.path.join(DATA, "social_profiles.txt")
OUTPUT_FILE = os.path.join(DATA, "extracted_emails.txt")

PLAIN_RE = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")

# patterns for the obfuscations people use to dodge scrapers
OBFUSCATED = [
    (re.compile(r"([A-Za-z0-9._%+\-]+)\s*\[\s*at\s*\]\s*"
                r"([A-Za-z0-9.\-]+)\s*\[\s*dot\s*\]\s*([A-Za-z]{2,})",
                re.I), "[at]/[dot]"),
    (re.compile(r"([A-Za-z0-9._%+\-]+)\s*\(\s*at\s*\)\s*"
                r"([A-Za-z0-9.\-]+)\s*\(\s*dot\s*\)\s*([A-Za-z]{2,})",
                re.I), "(at)/(dot)"),
    (re.compile(r"([A-Za-z0-9._%+\-]+)\s+at\s+([A-Za-z0-9\-]+)\s+dot\s+"
                r"([A-Za-z]{2,})", re.I), "word at/dot"),
    (re.compile(r"([A-Za-z0-9._%+\-]+)\s*<at>\s*([A-Za-z0-9.\-]+)\s*<dot>\s*"
                r"([A-Za-z]{2,})", re.I), "<at>/<dot>"),
]

SAMPLE = """@spandan_codes | SY CSE @ MIT-WPU | building MediVerse
Bio: DMs are slow, mail me on spandan.andhale@example.com
Website: spandan.dev

@riya_designs | UI/UX | Pune
Bio: collabs -> riya [at] designs [dot] studio
Not an email: 10/10 would recommend @riya_designs

@aman_backend | Go and Python | ex-intern
Bio: work enquiries: aman_k99 (at) sub.domain (dot) co
Also: aman.backend@gmail.com

@neha_qa | automation tester
Bio: reach me neha dot deshmukh at gmail dot com
Phone in bio: 90112-23344

@omkar.patil.dev | open source
Bio: omkar <at> example <dot> com | PGP key on request

@sana_devops | k8s | Mumbai
Bio: sana.shaikh@zoho.in - open to consulting
Pinned post: email support@mediverse.in for product questions

@no_contact_user | just lurking
Bio: no email, no DMs, nothing. @ me if you must.
Price: 50@kg for mangoes <- not an email either
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
        text = fh.read()

    profiles = [p for p in text.split("\n\n") if p.strip()]
    print(f"=== {len(profiles)} profile block(s) scanned ===")

    plain = PLAIN_RE.findall(text)
    print(f"\n=== plain addresses ({len(plain)}) ===")
    for e in plain:
        print("  ", e.lower())

    print("\n=== de-obfuscated addresses ===")
    recovered = []
    for pattern, label in OBFUSCATED:
        for match in pattern.finditer(text):
            local, domain, tld = match.groups()
            email = f"{local}@{domain}.{tld}".lower()
            recovered.append(email)
            print(f"  [{label:<12}] {match.group(0)[:44]!r:<48} -> {email}")
    if not recovered:
        print("  none")

    all_found = []
    for e in [x.lower() for x in plain] + recovered:
        if e not in all_found:
            all_found.append(e)

    print(f"\n=== per-profile breakdown ===")
    for block in profiles:
        handle = block.splitlines()[0].split("|")[0].strip()
        found = [e.lower() for e in PLAIN_RE.findall(block)]
        for pattern, _ in OBFUSCATED:
            for m in pattern.finditer(block):
                found.append(f"{m.group(1)}@{m.group(2)}.{m.group(3)}".lower())
        unique_here = []
        for e in found:
            if e not in unique_here:
                unique_here.append(e)
        status = ", ".join(unique_here) if unique_here else "(no email found)"
        print(f"  {handle:<24} {status}")

    print(f"\n=== final list: {len(all_found)} address(es) ===")
    for i, e in enumerate(all_found, 1):
        print(f"  {i:>2}. {e}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as fh:
        fh.write("\n".join(all_found) + "\n")
    print(f"\n  written to {OUTPUT_FILE}")

    print("\n=== false positives the pattern correctly avoids ===")
    for line in text.splitlines():
        if "@" in line and not PLAIN_RE.search(line):
            stripped = line.strip()
            if stripped:
                print(f"  {stripped[:62]}")

    print("\n=== note on scraping ===")
    print("  These profiles are synthetic text written by this script. A real")
    print("  scraper must honour each site's terms of service, robots.txt and")
    print("  the applicable data protection rules before collecting contacts.")
