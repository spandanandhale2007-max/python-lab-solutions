"""
Experiment 7 - Question 4: Data Breach Alert System

Scenario: After a data breach, identify leaked email addresses from a
compromised text file (leaked_data.txt). Use regex to extract and list all
unique email addresses for investigation.

Run: python q4_data_breach_alert.py

Note: this is a defensive exercise. The sample file below is synthetic data
written by this script; no real credentials are involved.
"""

import hashlib
import os
import re
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
INPUT_FILE = os.path.join(DATA, "leaked_data.txt")
OUTPUT_FILE = os.path.join(DATA, "breach_unique_emails.txt")
REPORT_FILE = os.path.join(DATA, "breach_report.txt")

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")

SAMPLE = """# synthetic dump used for a classroom exercise - no real accounts
id,email,password_hash,last_login
1,spandan.andhale@example.com,$2b$10$fakehashvalue001,2026-10-02
2,riya93@mitwpu.edu.in,$2b$10$fakehashvalue002,2026-10-04
3,AMAN_K99@sub.domain.co.in,$2b$10$fakehashvalue003,2026-09-28
4,neha.deshmukh@gmail.com,$2b$10$fakehashvalue004,2026-10-11
5,spandan.andhale@example.com,$2b$10$fakehashvalue005,2026-10-12
6,omkar.patil@example.com,$2b$10$fakehashvalue006,2026-08-19
7,corrupted-row-no-email,$2b$10$fakehashvalue007,2026-07-01
8,sana.shaikh@zoho.in,$2b$10$fakehashvalue008,2026-10-13
9,admin@mediverse.in,$2b$10$fakehashvalue009,2026-10-14
10,support@mediverse.in,$2b$10$fakehashvalue010,2026-10-14
11,Riya93@MITWPU.EDU.IN,$2b$10$fakehashvalue011,2026-10-15
12,billing@partnerclinic.co.uk,$2b$10$fakehashvalue012,2026-06-30
free text appended by the attacker: contact me at ransom.note@darkmail.invalid
"""

INTERNAL_DOMAINS = {"mediverse.in"}


def ensure_sample():
    os.makedirs(DATA, exist_ok=True)
    if not os.path.exists(INPUT_FILE):
        with open(INPUT_FILE, "w", encoding="utf-8") as fh:
            fh.write(SAMPLE)
        print(f"[setup] created sample input {INPUT_FILE}")


def pseudonymise(email):
    """For sharing counts without re-exposing the addresses."""
    return hashlib.sha256(email.encode()).hexdigest()[:16]


if __name__ == "__main__":
    ensure_sample()

    with open(INPUT_FILE, "r", encoding="utf-8") as fh:
        text = fh.read()
    lines = text.splitlines()

    print(f"=== scanning {INPUT_FILE} ===")
    print(f"  lines   : {len(lines)}")
    print(f"  bytes   : {len(text):,}")

    raw_hits = EMAIL_RE.findall(text)
    normalised = [e.lower() for e in raw_hits]

    print(f"\n=== {len(raw_hits)} match(es), "
          f"{len(set(normalised))} unique after normalising case ===")

    unique = []
    for e in normalised:
        if e not in unique:
            unique.append(e)

    print("\n=== unique leaked addresses ===")
    counts = Counter(normalised)
    print(f"  {'#':<4}{'email':<40}{'occurrences':>12}{'pseudonym':>20}")
    for i, e in enumerate(unique, 1):
        print(f"  {i:<4}{e:<40}{counts[e]:>12}{pseudonymise(e):>20}")

    print("\n=== case-variant duplicates found by normalising ===")
    variants = {}
    for e in raw_hits:
        variants.setdefault(e.lower(), set()).add(e)
    for low, forms in variants.items():
        if len(forms) > 1:
            print(f"  {low:<40} appeared as {sorted(forms)}")

    internal = [e for e in unique if e.split("@")[1] in INTERNAL_DOMAINS]
    external = [e for e in unique if e.split("@")[1] not in INTERNAL_DOMAINS]

    print("\n=== triage ===")
    print(f"  internal/company accounts ({len(internal)}): {internal}")
    print(f"  external customer accounts ({len(external)}): {len(external)} "
          f"addresses")
    print(f"  attacker-supplied address found: "
          f"{[e for e in unique if 'darkmail' in e] or 'none'}")

    print("\n=== rows that leaked no address (data quality) ===")
    for n, line in enumerate(lines, 1):
        if line.strip() and not line.startswith("#") and \
                not EMAIL_RE.search(line) and "," in line:
            print(f"  line {n}: {line.strip()[:60]}")

    print("\n=== affected domains ===")
    domains = Counter(e.split("@")[1] for e in unique)
    for d, c in domains.most_common():
        tag = "  <- internal" if d in INTERNAL_DOMAINS else ""
        print(f"  {d:<30} {c} account(s){tag}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as fh:
        fh.write("\n".join(unique) + "\n")

    with open(REPORT_FILE, "w", encoding="utf-8") as fh:
        fh.write("DATA BREACH - PRELIMINARY SCAN REPORT\n")
        fh.write(f"source file            : {os.path.basename(INPUT_FILE)}\n")
        fh.write(f"lines scanned          : {len(lines)}\n")
        fh.write(f"email matches          : {len(raw_hits)}\n")
        fh.write(f"unique accounts        : {len(unique)}\n")
        fh.write(f"internal accounts      : {len(internal)}\n")
        fh.write(f"external accounts      : {len(external)}\n")
        fh.write(f"affected domains       : {len(domains)}\n\n")
        fh.write("unique accounts (pseudonymised for sharing):\n")
        for e in unique:
            fh.write(f"  {pseudonymise(e)}  {e.split('@')[1]}\n")

    print(f"\n  unique list written to : {OUTPUT_FILE}")
    print(f"  report written to      : {REPORT_FILE}")

    print("\n=== recommended next steps ===")
    print("  1. force a password reset for all "
          f"{len(unique)} affected accounts")
    print("  2. revoke active sessions and API tokens")
    print(f"  3. notify the {len(external)} external users within 72 hours")
    print("  4. rotate credentials for the internal accounts first: "
          f"{internal}")
    print("  5. preserve the original dump as evidence, work on copies only")
