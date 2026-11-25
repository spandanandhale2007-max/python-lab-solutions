"""
Experiment 8 - Question 8: Email Archive Preview

Scenario: An email application archives raw emails in email_archive.txt. Read
the archive, count how many emails (lines) there are, extract the first two
and save them to email_preview.txt.

Run: python q8_email_archive_preview.py
"""

import os
import re
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
INPUT_FILE = os.path.join(DATA, "email_archive.txt")
OUTPUT_FILE = os.path.join(DATA, "email_preview.txt")

ROW_RE = re.compile(r"^(?P<date>\d{4}-\d{2}-\d{2})\s+\|\s+"
                    r"(?P<sender>[^|]+)\s+\|\s+(?P<subject>[^|]+)\s+\|\s+"
                    r"(?P<flags>.*)$")

SAMPLE = """2026-11-20 | coordinator@mitwpu.edu.in | Project review slot confirmed | unread,important
2026-11-20 | riya93@mitwpu.edu.in | Re: screenshots for the deck | read
2026-11-21 | noreply@netlify.com | Deploy succeeded for mediverse | read
2026-11-21 | aman_k99@sub.domain.co.in | Pull request #14 ready | unread
2026-11-22 | noreply@github.com | [MediVerse] 2 new issues opened | read
2026-11-22 | support@supabase.io | Your project usage this month | read
2026-11-23 | coordinator@mitwpu.edu.in | Reminder: submit by 30 November | unread,important
2026-11-23 | spam.offers@deals.top | YOU WON a free laptop!! | spam
2026-11-24 | neha.deshmukh@gmail.com | Can you review my pandas notebook | unread
2026-11-24 | noreply@netlify.com | Deploy failed for mediverse | unread,important
2026-11-25 | riya93@mitwpu.edu.in | Final deck draft attached | unread
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
        lines = [ln.rstrip("\n") for ln in fh if ln.strip()]

    print(f"=== read {os.path.basename(INPUT_FILE)} ===")
    print(f"  emails archived (lines) : {len(lines)}")
    print(f"  file size               : {os.path.getsize(INPUT_FILE)} bytes")

    mails = []
    for line in lines:
        m = ROW_RE.match(line)
        if m:
            mails.append({
                "date": m.group("date"),
                "sender": m.group("sender").strip(),
                "subject": m.group("subject").strip(),
                "flags": [f.strip() for f in m.group("flags").split(",")
                          if f.strip()],
            })
    print(f"  parsed successfully     : {len(mails)}")

    first_two = lines[:2]
    print("\n=== first two emails ===")
    for i, line in enumerate(first_two, 1):
        print(f"  {i}. {line}")

    print("\n=== inbox listing ===")
    print(f"  {'date':<12}{'from':<36}{'subject':<38}flags")
    print("  " + "-" * 104)
    for m in mails:
        marker = "*" if "important" in m["flags"] else " "
        print(f"{marker} {m['date']:<12}{m['sender'][:34]:<36}"
              f"{m['subject'][:36]:<38}{','.join(m['flags'])}")

    unread = [m for m in mails if "unread" in m["flags"]]
    important = [m for m in mails if "important" in m["flags"]]
    spam = [m for m in mails if "spam" in m["flags"]]

    print("\n=== counts ===")
    print(f"  total   : {len(mails)}")
    print(f"  unread  : {len(unread)}")
    print(f"  important: {len(important)}")
    print(f"  spam    : {len(spam)}")
    print(f"  read    : {len(mails) - len(unread) - len(spam)}")

    print("\n=== top senders ===")
    senders = Counter(m["sender"] for m in mails)
    for sender, count in senders.most_common():
        print(f"  {sender:<40}{count}")

    print("\n=== domains ===")
    domains = Counter(m["sender"].split("@")[1] for m in mails)
    for d, c in domains.most_common():
        print(f"  {d:<26}{c}")

    print("\n=== needs a reply (unread and important) ===")
    for m in mails:
        if "unread" in m["flags"] and "important" in m["flags"]:
            print(f"  {m['date']}  {m['sender']:<36}{m['subject']}")

    print("\n=== emails per day ===")
    per_day = Counter(m["date"] for m in mails)
    for day in sorted(per_day):
        print(f"  {day}  {per_day[day]}  {'#' * per_day[day]}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as fh:
        fh.write(f"Emails in archive: {len(lines)}\n")
        for line in first_two:
            fh.write(line + "\n")

    print(f"\n=== wrote {OUTPUT_FILE} ===")
    with open(OUTPUT_FILE, "r", encoding="utf-8") as fh:
        for line in fh:
            print("  " + line.rstrip())
    print(f"\n  preview file: "
          f"{sum(1 for _ in open(OUTPUT_FILE, encoding='utf-8'))} line(s), "
          f"{os.path.getsize(OUTPUT_FILE)} bytes")
