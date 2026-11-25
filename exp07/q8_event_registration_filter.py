"""
Experiment 7 - Question 8: Event Registration Email Filter

Scenario: An event registration form allows free text and the entries are
saved in registration_entries.txt. Use regex to find and validate the entered
email addresses for sending event details.

Run: python q8_event_registration_filter.py
"""

import os
import re
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
INPUT_FILE = os.path.join(DATA, "registration_entries.txt")
VALID_FILE = os.path.join(DATA, "event_mailing_list.txt")
FIX_FILE = os.path.join(DATA, "entries_needing_correction.txt")

CANDIDATE_RE = re.compile(r"[^\s,;|]+@[^\s,;|]+")
STRICT_RE = re.compile(
    r"^[A-Za-z0-9](?:[A-Za-z0-9._%+\-]*[A-Za-z0-9])?@"
    r"(?:[A-Za-z0-9](?:[A-Za-z0-9\-]*[A-Za-z0-9])?\.)+[A-Za-z]{2,}$"
)
ENTRY_RE = re.compile(r"^(?P<id>REG-\d+)\s*\|\s*(?P<rest>.*)$")

# common typos worth auto-suggesting
DOMAIN_FIXES = {
    "gmial.com": "gmail.com", "gmai.com": "gmail.com", "gmail.co": "gmail.com",
    "yahooo.com": "yahoo.com", "hotmai.com": "hotmail.com",
    "outlok.com": "outlook.com",
}

SAMPLE = """REG-001 | Spandan Andhale, SY CSE, spandan.andhale@example.com, veg meal
REG-002 | Riya Sharma riya93@mitwpu.edu.in needs a parking pass
REG-003 | Aman Kulkarni aman_k99@gmial.com (typo in domain?)
REG-004 | Neha Deshmukh - neha.deshmukh@gmail.com - attending both days
REG-005 | Omkar Patil omkar.patil@ (incomplete)
REG-006 | Sana Shaikh | sana.shaikh@zoho.in | vegan meal
REG-007 | Rohit Jadhav rohitjadhav.gmail.com (forgot the @)
REG-008 | Pooja Nair pooja..nair@example.com
REG-009 | Kiran Rao kiran.rao@diagnostics.example.net
REG-010 | Tanvi Gokhale TANVI.GOKHALE@MITWPU.EDU.IN
REG-011 | Harsh Mehta harsh@mehta@example.com
REG-012 | Walk-in registration, contact number only: 90112-23344
REG-013 | Spandan Andhale spandan.andhale@example.com duplicate entry
REG-014 | Dr. Kavita Rao kavita.rao@healthblog.example.org, speaker
REG-015 | Sameer Khan sameer@short.c
"""


def ensure_sample():
    os.makedirs(DATA, exist_ok=True)
    if not os.path.exists(INPUT_FILE):
        with open(INPUT_FILE, "w", encoding="utf-8") as fh:
            fh.write(SAMPLE)
        print(f"[setup] created sample input {INPUT_FILE}")


def diagnose(token):
    t = token.strip().strip(".,;:()<>[]\"'")
    if t.count("@") == 0:
        return "no @ sign"
    if t.count("@") > 1:
        return "more than one @"
    local, _, domain = t.partition("@")
    if not local:
        return "empty local part"
    if not domain:
        return "domain missing"
    if ".." in t:
        return "consecutive dots"
    if "." not in domain:
        return "domain has no dot"
    if len(domain.rsplit(".", 1)[1]) < 2:
        return "top level domain too short"
    return "malformed"


def suggest(token):
    t = token.strip().strip(".,;:()<>[]\"'").lower()
    if "@" in t:
        local, _, domain = t.partition("@")
        if domain in DOMAIN_FIXES:
            return f"{local}@{DOMAIN_FIXES[domain]}"
    if "@" not in t and t.count(".") >= 2:
        # someone typed name.gmail.com instead of name@gmail.com
        head, _, tail = t.rpartition(".")
        parts = head.rsplit(".", 1)
        if len(parts) == 2:
            return f"{parts[0]}@{parts[1]}.{tail}"
    return None


if __name__ == "__main__":
    ensure_sample()

    with open(INPUT_FILE, "r", encoding="utf-8") as fh:
        lines = [ln for ln in fh.read().splitlines() if ln.strip()]

    print(f"=== {len(lines)} registration entry(ies) ===")

    valid, problems = [], []
    for line in lines:
        m = ENTRY_RE.match(line)
        reg_id = m.group("id") if m else "(no id)"
        rest = m.group("rest") if m else line
        tokens = CANDIDATE_RE.findall(rest)
        if not tokens:
            problems.append((reg_id, "(none)", "no email in the entry", None))
            continue
        for token in tokens:
            cleaned = token.strip().strip(".,;:()<>[]\"'")
            if STRICT_RE.match(cleaned):
                valid.append((reg_id, cleaned.lower()))
            else:
                problems.append((reg_id, token, diagnose(token),
                                 suggest(token)))

    print(f"\n=== {len(valid)} valid address(es) ===")
    for reg_id, email in valid:
        print(f"  {reg_id:<9} {email}")

    print(f"\n=== {len(problems)} entry(ies) needing correction ===")
    print(f"  {'id':<9}{'as typed':<32}{'problem':<28}suggestion")
    print("  " + "-" * 92)
    for reg_id, token, why, fix in problems:
        print(f"  {reg_id:<9}{token[:30]:<32}{why:<28}{fix or '-'}")

    mailing_list = []
    for _, email in valid:
        if email not in mailing_list:
            mailing_list.append(email)

    counts = Counter(e for _, e in valid)
    print(f"\n=== final mailing list: {len(mailing_list)} recipient(s) ===")
    for i, e in enumerate(mailing_list, 1):
        note = f"  (registered {counts[e]} times)" if counts[e] > 1 else ""
        print(f"  {i:>2}. {e}{note}")
    print(f"  duplicate registrations removed: {len(valid) - len(mailing_list)}")

    print(f"\n=== registration statistics ===")
    print(f"  entries submitted      : {len(lines)}")
    print(f"  contactable attendees  : {len(mailing_list)}")
    print(f"  entries to chase up    : {len(problems)}")
    print(f"  data quality           : "
          f"{len(mailing_list) / len(lines) * 100:.1f}% usable")
    fixable = sum(1 for *_, fix in problems if fix)
    print(f"  auto-fixable typos     : {fixable}")

    domains = Counter(e.split("@")[1] for e in mailing_list)
    print(f"\n=== attendee domains ===")
    for d, c in domains.most_common():
        print(f"  {d:<34} {c}")

    with open(VALID_FILE, "w", encoding="utf-8") as fh:
        fh.write("\n".join(mailing_list) + "\n")
    with open(FIX_FILE, "w", encoding="utf-8") as fh:
        fh.write("id\tas_typed\tproblem\tsuggestion\n")
        for reg_id, token, why, fix in problems:
            fh.write(f"{reg_id}\t{token}\t{why}\t{fix or ''}\n")

    print(f"\n  mailing list written to : {VALID_FILE}")
    print(f"  corrections written to  : {FIX_FILE}")
