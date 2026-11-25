"""
Experiment 7 - Question 10: Spam Detector System

Scenario: Analyse potentially spammy content from user messages
(spam_check.txt). Use regex to find and flag messages that include suspicious
email addresses for further inspection.

Run: python q10_spam_detector.py
"""

import os
import re
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
INPUT_FILE = os.path.join(DATA, "spam_check.txt")
OUTPUT_FILE = os.path.join(DATA, "flagged_messages.txt")

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
MSG_RE = re.compile(r"^(?P<id>MSG-\d+)\s*\|\s*(?P<sender>\S+)\s*\|\s*"
                    r"(?P<body>.*)$")

SUSPICIOUS_TLDS = {"invalid", "top", "xyz", "click", "zip", "loan", "win"}
DISPOSABLE = {"mailinator.com", "tempmail.com", "guerrillamail.com",
              "10minutemail.com", "throwaway.email"}
SPAM_WORDS = ["winner", "lottery", "free money", "click here", "urgent",
              "prize", "crypto", "double your", "verify your account",
              "wire transfer", "bank details", "act now", "limited offer"]
RANDOM_LOCAL = re.compile(r"^[a-z]{0,3}\d{4,}[a-z0-9]*$|^[a-z0-9]{16,}$")

SAMPLE = """MSG-001 | spandan.andhale@example.com | Hi, the bed availability page throws an error. Can you check?
MSG-002 | winner27381@mailinator.com | CONGRATULATIONS!! You are our lottery WINNER. Claim your prize now, click here: http://claim.win
MSG-003 | riya93@mitwpu.edu.in | Sharing the project report for review. Deadline is Friday.
MSG-004 | support@mediverse.in | Scheduled maintenance tonight from 1 AM to 3 AM.
MSG-005 | crypto.doubler@gains.top | Double your money in 24 hours. Send BTC to this wallet. ACT NOW, limited offer!
MSG-006 | aman_k99@sub.domain.co.in | Refund request for appointment APP-7781.
MSG-007 | security-alert@mediverse-in.xyz | URGENT: verify your account or it will be closed. Reply with your bank details.
MSG-008 | a9f83kd92jdk19dkq@throwaway.email | free money free money free money
MSG-009 | neha.deshmukh@gmail.com | Please update my registered phone number.
MSG-010 | hr@medsupplies.example.in | Invoice attached for the October supply order.
MSG-011 | no-reply@ransom.note.invalid | We have your records. Wire transfer 2 BTC or we publish them.
MSG-012 | kavita.rao@healthblog.example.org | Would you like to co-author an article on hospital data?
"""


def ensure_sample():
    os.makedirs(DATA, exist_ok=True)
    if not os.path.exists(INPUT_FILE):
        with open(INPUT_FILE, "w", encoding="utf-8") as fh:
            fh.write(SAMPLE)
        print(f"[setup] created sample input {INPUT_FILE}")


def score_email(email):
    """Returns (points, list of reasons)."""
    points, reasons = 0, []
    local, _, domain = email.lower().partition("@")
    tld = domain.rsplit(".", 1)[-1]

    if tld in SUSPICIOUS_TLDS:
        points += 3
        reasons.append(f"suspicious TLD .{tld}")
    if domain in DISPOSABLE:
        points += 3
        reasons.append("disposable mail provider")
    if RANDOM_LOCAL.match(local):
        points += 2
        reasons.append("machine-generated local part")
    if len(local) > 20:
        points += 1
        reasons.append("unusually long local part")
    if sum(c.isdigit() for c in local) >= 4:
        points += 1
        reasons.append("many digits in the local part")
    if domain.count("-") >= 1 and any(
            brand in domain for brand in ("mediverse", "paypal", "sbi")):
        points += 3
        reasons.append("look-alike domain impersonating a brand")
    return points, reasons


def score_body(body):
    points, hits = 0, []
    low = body.lower()
    for word in SPAM_WORDS:
        if word in low:
            points += 1
            hits.append(word)
    caps = sum(1 for c in body if c.isupper())
    if body and caps / len(body) > 0.30:
        points += 2
        hits.append("excessive capitals")
    if body.count("!") >= 2:
        points += 1
        hits.append("multiple exclamation marks")
    return points, hits


if __name__ == "__main__":
    ensure_sample()

    with open(INPUT_FILE, "r", encoding="utf-8") as fh:
        lines = [ln for ln in fh.read().splitlines() if ln.strip()]

    print(f"=== {len(lines)} message(s) to inspect ===")

    results = []
    for line in lines:
        m = MSG_RE.match(line)
        if not m:
            continue
        sender = m.group("sender")
        body = m.group("body")
        body_emails = [e.lower() for e in EMAIL_RE.findall(body)]
        e_points, e_reasons = score_email(sender)
        b_points, b_hits = score_body(body)
        total = e_points + b_points
        results.append({
            "id": m.group("id"), "sender": sender.lower(), "body": body,
            "email_points": e_points, "email_reasons": e_reasons,
            "body_points": b_points, "body_hits": b_hits,
            "score": total,
            "verdict": ("SPAM" if total >= 5 else
                        "SUSPECT" if total >= 2 else "CLEAN"),
            "embedded": body_emails,
        })

    print(f"\n=== verdicts ===")
    print(f"  {'id':<9}{'sender':<40}{'email':>6}{'body':>6}{'score':>7}"
          f"  verdict")
    print("  " + "-" * 78)
    for r in results:
        print(f"  {r['id']:<9}{r['sender'][:38]:<40}{r['email_points']:>6}"
              f"{r['body_points']:>6}{r['score']:>7}  {r['verdict']}")

    print("\n=== flagged messages in detail ===")
    for r in results:
        if r["verdict"] == "CLEAN":
            continue
        print(f"\n  {r['id']} [{r['verdict']}, score {r['score']}]")
        print(f"    sender : {r['sender']}")
        print(f"    body   : {r['body'][:70]}")
        if r["email_reasons"]:
            print(f"    address flags : {', '.join(r['email_reasons'])}")
        if r["body_hits"]:
            print(f"    content flags : {', '.join(r['body_hits'])}")
        if r["embedded"]:
            print(f"    embedded addresses: {r['embedded']}")

    counts = Counter(r["verdict"] for r in results)
    print(f"\n=== summary ===")
    for verdict in ("SPAM", "SUSPECT", "CLEAN"):
        print(f"  {verdict:<9}{counts.get(verdict, 0):>3} message(s)")
    print(f"  spam rate: "
          f"{counts.get('SPAM', 0) / len(results) * 100:.1f}%")

    print("\n=== sender domains by verdict ===")
    for verdict in ("SPAM", "SUSPECT", "CLEAN"):
        domains = sorted({r["sender"].split("@")[1] for r in results
                          if r["verdict"] == verdict})
        print(f"  {verdict:<9}{domains}")

    print("\n=== blocklist suggestion ===")
    block = sorted({r["sender"].split("@")[1] for r in results
                    if r["verdict"] == "SPAM"})
    for d in block:
        print(f"  block domain: {d}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as fh:
        fh.write("id\tverdict\tscore\tsender\treasons\n")
        for r in results:
            if r["verdict"] != "CLEAN":
                reasons = "; ".join(r["email_reasons"] + r["body_hits"])
                fh.write(f"{r['id']}\t{r['verdict']}\t{r['score']}\t"
                         f"{r['sender']}\t{reasons}\n")
    print(f"\n  flagged messages written to {OUTPUT_FILE}")

    print("\n=== note ===")
    print("  This is a rule-based filter for a lab exercise. Real spam")
    print("  filtering combines such signals with sender reputation, SPF,")
    print("  DKIM and DMARC checks, and a trained classifier.")
