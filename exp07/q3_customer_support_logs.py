"""
Experiment 7 - Question 3: Customer Support Logs

Scenario: Customer support logs are saved in support_log.txt and include
complaints together with contact details. Use regex to extract customer email
addresses for follow-up.

Run: python q3_customer_support_logs.py
"""

import os
import re
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
INPUT_FILE = os.path.join(DATA, "support_log.txt")
OUTPUT_FILE = os.path.join(DATA, "followup_emails.txt")

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
# a log line looks like: 2026-11-18 09:14 [P1] TICKET-4411 <email> message
LINE_RE = re.compile(
    r"^(?P<date>\d{4}-\d{2}-\d{2})\s+(?P<time>\d{2}:\d{2})\s+"
    r"\[(?P<priority>P[1-4])\]\s+(?P<ticket>TICKET-\d+)\s+"
    r"(?P<rest>.*)$"
)

SAMPLE = """2026-11-18 09:14 [P1] TICKET-4411 spandan.andhale@example.com App crashes when I open the bed availability page. Urgent.
2026-11-18 09:40 [P3] TICKET-4412 riya93@mitwpu.edu.in Cannot reset my password, the OTP never arrives.
2026-11-18 10:02 [P2] TICKET-4413 no contact details given, caller rang from 020-2555-1234
2026-11-18 10:35 [P1] TICKET-4414 aman_k99@sub.domain.co.in Double charged for the same appointment booking.
2026-11-18 11:11 [P4] TICKET-4415 Please update my address, reach me at neha.deshmukh+support@gmail.com
2026-11-18 12:20 [P2] TICKET-4416 spandan.andhale@example.com Follow up on TICKET-4411, still broken.
2026-11-19 08:05 [P3] TICKET-4417 omkar.patil@example.com Requesting an invoice copy for October.
2026-11-19 09:30 [P1] TICKET-4418 sana.shaikh@zoho.in Doctor list shows the wrong department.
2026-11-19 10:00 [P4] TICKET-4419 feedback at mediverse dot in (obfuscated, unusable)
2026-11-19 11:45 [P2] TICKET-4420 riya93@mitwpu.edu.in Password reset worked, closing the ticket. Thanks!
2026-11-19 14:10 [P1] TICKET-4421 escalation@partnerclinic.co.uk Patient records failed to sync overnight.
2026-11-20 09:00 [P3] TICKET-4422 aman_k99@sub.domain.co.in Refund still not credited.
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
        lines = [ln for ln in fh.read().splitlines() if ln.strip()]

    print(f"=== {len(lines)} support log line(s) parsed ===")

    records = []
    unparsed = []
    for raw in lines:
        m = LINE_RE.match(raw)
        if not m:
            unparsed.append(raw)
            continue
        emails = EMAIL_RE.findall(m.group("rest"))
        records.append({
            "date": m.group("date"),
            "time": m.group("time"),
            "priority": m.group("priority"),
            "ticket": m.group("ticket"),
            "email": emails[0].lower() if emails else None,
            "message": EMAIL_RE.sub("", m.group("rest")).strip(),
        })

    print(f"\n=== parsed tickets ===")
    print(f"  {'ticket':<13}{'date':<12}{'pri':<5}{'email':<38}message")
    print("  " + "-" * 100)
    for r in records:
        email = r["email"] or "(none found)"
        print(f"  {r['ticket']:<13}{r['date']:<12}{r['priority']:<5}"
              f"{email:<38}{r['message'][:34]}")

    if unparsed:
        print(f"\n  {len(unparsed)} line(s) did not match the log format")

    with_email = [r for r in records if r["email"]]
    without = [r for r in records if not r["email"]]
    print(f"\n=== contactability ===")
    print(f"  tickets with an email    : {len(with_email)}")
    print(f"  tickets without an email : {len(without)} "
          f"-> {[r['ticket'] for r in without]}")

    unique = []
    for r in with_email:
        if r["email"] not in unique:
            unique.append(r["email"])
    print(f"\n=== {len(unique)} unique customer(s) to follow up ===")
    counts = Counter(r["email"] for r in with_email)
    for email in unique:
        tickets = [r["ticket"] for r in with_email if r["email"] == email]
        worst = min((r["priority"] for r in with_email if r["email"] == email))
        print(f"  {email:<38} {counts[email]} ticket(s) {tickets} "
              f"highest priority {worst}")

    print("\n=== repeat complainants (2 or more tickets) ===")
    repeats = [(e, c) for e, c in counts.items() if c > 1]
    for email, c in sorted(repeats, key=lambda kv: -kv[1]):
        print(f"  {email:<38} {c} tickets - call this customer")
    if not repeats:
        print("  none")

    print("\n=== P1 escalation list ===")
    p1 = [r for r in with_email if r["priority"] == "P1"]
    for r in p1:
        print(f"  {r['ticket']}  {r['email']:<38} {r['message'][:40]}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as fh:
        fh.write("# follow-up list generated from support_log.txt\n")
        for email in unique:
            tickets = ",".join(r["ticket"] for r in with_email
                               if r["email"] == email)
            fh.write(f"{email}\t{counts[email]}\t{tickets}\n")
    print(f"\n  follow-up list written to {OUTPUT_FILE}")

    print("\n=== domain summary ===")
    domains = Counter(e.split("@")[1] for e in unique)
    for d, c in domains.most_common():
        print(f"  {d:<26} {c}")
