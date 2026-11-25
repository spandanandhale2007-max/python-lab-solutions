"""
Experiment 7 - Question 1: Job Application Scraper

Scenario: The HR department receives hundreds of job applications in a text
file (applications.txt). Use regex to extract all email addresses so HR can
contact the applicants. Save the emails in emails_list.txt.

Run: python q1_job_application_scraper.py
The sample applications.txt is created automatically if it does not exist.
"""

import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
INPUT_FILE = os.path.join(DATA, "applications.txt")
OUTPUT_FILE = os.path.join(DATA, "emails_list.txt")

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")

SAMPLE = """Application ID: APP-1001
Name: Spandan Andhale
Position: Python Developer Intern
Contact: spandan.andhale@example.com | +91 90112 23344
Cover note: I have built a hospital management app in React and Python.

Application ID: APP-1002
Name: Riya Sharma
Position: Data Analyst
Reach me at riya.sharma93@mitwpu.edu.in or on LinkedIn.

Application ID: APP-1003
Name: Aman Kulkarni
Position: Backend Engineer
Email: aman_k99@sub.domain.co.in
Alternate: amank.work+jobs@gmail.com

Application ID: APP-1004
Name: Neha Deshmukh
Position: QA Engineer
Phone only, no email provided. Call 020-2555-1234.

Application ID: APP-1005
Name: Omkar Patil
Position: Python Developer Intern
Mail: OMKAR.PATIL@Example.COM (please use this one)
Referred by spandan.andhale@example.com

Application ID: APP-1006
Name: Sana Shaikh
Position: DevOps Trainee
Contact: sana [at] shaikh [dot] com   <- obfuscated, not a valid address
Backup: sana.shaikh@zoho.in
"""


def ensure_sample():
    os.makedirs(DATA, exist_ok=True)
    if not os.path.exists(INPUT_FILE):
        with open(INPUT_FILE, "w", encoding="utf-8") as fh:
            fh.write(SAMPLE)
        print(f"[setup] created sample input {INPUT_FILE}")


def extract_emails(path):
    with open(path, "r", encoding="utf-8") as fh:
        text = fh.read()
    return EMAIL_RE.findall(text), text


if __name__ == "__main__":
    ensure_sample()

    emails, text = extract_emails(INPUT_FILE)

    print(f"=== read {INPUT_FILE} ===")
    print(f"  characters : {len(text):,}")
    print(f"  lines      : {len(text.splitlines())}")
    print(f"  applications: {text.count('Application ID')}")

    print(f"\n=== regex pattern ===")
    print(f"  {EMAIL_RE.pattern}")

    print(f"\n=== {len(emails)} email(s) matched, in order of appearance ===")
    for i, e in enumerate(emails, 1):
        print(f"  {i:>2}. {e}")

    # normalise and keep the order of first appearance
    unique = []
    for e in emails:
        low = e.lower()
        if low not in unique:
            unique.append(low)

    print(f"\n=== {len(unique)} unique address(es) after lowercasing ===")
    for i, e in enumerate(unique, 1):
        print(f"  {i:>2}. {e}")
    duplicates = len(emails) - len(unique)
    if duplicates:
        print(f"  ({duplicates} duplicate reference(s) removed)")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as fh:
        fh.write("\n".join(unique) + "\n")
    print(f"\n=== written to {OUTPUT_FILE} ===")
    with open(OUTPUT_FILE, "r", encoding="utf-8") as fh:
        print("".join(f"  {line}" for line in fh))

    print("=== grouping by domain, useful for HR reporting ===")
    domains = {}
    for e in unique:
        domains.setdefault(e.split("@")[1], []).append(e)
    for domain, members in sorted(domains.items()):
        print(f"  {domain:<22} {len(members)}  {members}")

    print("\n=== lines that mentioned no usable address ===")
    for n, line in enumerate(text.splitlines(), 1):
        if ("[at]" in line.lower()) or ("no email" in line.lower()):
            print(f"  line {n}: {line.strip()}")
