# Experiment 7 - Unit III

Regular expressions: extracting and validating email addresses

10 scenario questions, each solved in its own section and its own file. Every program below was executed and the real output is included.

[Back to the index](../README.md)

---

## Questions in this experiment

- [Experiment 7 - Question 1: Job Application Scraper](#experiment-7---question-1-job-application-scraper)
- [Experiment 7 - Question 2: Newsletter Subscription Validator](#experiment-7---question-2-newsletter-subscription-validator)
- [Experiment 7 - Question 3: Customer Support Logs](#experiment-7---question-3-customer-support-logs)
- [Experiment 7 - Question 4: Data Breach Alert System](#experiment-7---question-4-data-breach-alert-system)
- [Experiment 7 - Question 5: Social Media Profile Extractor](#experiment-7---question-5-social-media-profile-extractor)
- [Experiment 7 - Question 6: Marketing Campaign Contacts](#experiment-7---question-6-marketing-campaign-contacts)
- [Experiment 7 - Question 7: Classroom Group Project Submissions](#experiment-7---question-7-classroom-group-project-submissions)
- [Experiment 7 - Question 8: Event Registration Email Filter](#experiment-7---question-8-event-registration-email-filter)
- [Experiment 7 - Question 9: Resume Parser Tool](#experiment-7---question-9-resume-parser-tool)
- [Experiment 7 - Question 10: Spam Detector System](#experiment-7---question-10-spam-detector-system)

---

## Experiment 7 - Question 1: Job Application Scraper

Scenario: The HR department receives hundreds of job applications in a text
file (applications.txt). Use regex to extract all email addresses so HR can
contact the applicants. Save the emails in emails_list.txt.

Run: python q1_job_application_scraper.py
The sample applications.txt is created automatically if it does not exist.

**File:** [`q1_job_application_scraper.py`](q1_job_application_scraper.py) &nbsp;&middot;&nbsp; **Run:** `python q1_job_application_scraper.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
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
```

</details>

<details>
<summary>Program output</summary>

```text
=== read d:\Claude- Hospitalisation Services\python-lab-solutions\exp07\data\applications.txt ===
  characters : 933
  lines      : 33
  applications: 6

=== regex pattern ===
  [A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}

=== 7 email(s) matched, in order of appearance ===
   1. spandan.andhale@example.com
   2. riya.sharma93@mitwpu.edu.in
   3. aman_k99@sub.domain.co.in
   4. amank.work+jobs@gmail.com
   5. OMKAR.PATIL@Example.COM
   6. spandan.andhale@example.com
   7. sana.shaikh@zoho.in

=== 6 unique address(es) after lowercasing ===
   1. spandan.andhale@example.com
   2. riya.sharma93@mitwpu.edu.in
   3. aman_k99@sub.domain.co.in
   4. amank.work+jobs@gmail.com
   5. omkar.patil@example.com
   6. sana.shaikh@zoho.in
  (1 duplicate reference(s) removed)

=== written to d:\Claude- Hospitalisation Services\python-lab-solutions\exp07\data\emails_list.txt ===
  spandan.andhale@example.com
  riya.sharma93@mitwpu.edu.in
  aman_k99@sub.domain.co.in
  amank.work+jobs@gmail.com
  omkar.patil@example.com
  sana.shaikh@zoho.in

=== grouping by domain, useful for HR reporting ===
  example.com            2  ['spandan.andhale@example.com', 'omkar.patil@example.com']
  gmail.com              1  ['amank.work+jobs@gmail.com']
  mitwpu.edu.in          1  ['riya.sharma93@mitwpu.edu.in']
  sub.domain.co.in       1  ['aman_k99@sub.domain.co.in']
  zoho.in                1  ['sana.shaikh@zoho.in']

=== lines that mentioned no usable address ===
  line 21: Phone only, no email provided. Call 020-2555-1234.
  line 32: Contact: sana [at] shaikh [dot] com   <- obfuscated, not a valid address

```

</details>

---

## Experiment 7 - Question 2: Newsletter Subscription Validator

Scenario: A website collects emails for a newsletter. The raw submissions are
stored in submissions.txt, which includes noise text. Use regex to extract
only the valid email addresses for building the subscriber list.

Run: python q2_newsletter_validator.py

**File:** [`q2_newsletter_validator.py`](q2_newsletter_validator.py) &nbsp;&middot;&nbsp; **Run:** `python q2_newsletter_validator.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
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
```

</details>

<details>
<summary>Program output</summary>

```text
=== 22 raw submission line(s) read ===

=== 12 valid address(es) ===
  line  1: spandan.andhale@example.com
  line  2: riya93@mitwpu.edu.in
  line  3: aman_k99@sub.domain.co.in
  line 11: name@domain.com
  line 13: upper.case@example.com
  line 14: spandan.andhale@example.com
  line 15: neha+newsletter@gmail.com
  line 16: sana.shaikh@zoho.in
  line 17: omkar..patil@example.com
  line 18: hello_world-123@my-domain.org
  line 20: feedback@company.co.uk
  line 21: support@mediverse.in

=== 10 rejection(s) with the reason ===
  line  4: not.an.email.at.all                      -> contains no @ candidate at all
  line  5: @nolocalpart.com                         -> contains no @ candidate at all
  line  6: missing-domain@                          -> contains no @ candidate at all
  line  7: double@@at.com                           -> multiple @ signs
  line  8: user@nodot                               -> domain has no dot (no TLD)
  line  9: trailing.dot@domain.                     -> domain ends with a dot
  line 10: .leading.dot@domain.com                  -> local part starts or ends with a dot
  line 12: too@short.c                              -> top level domain too short
  line 19: admin@localhost                          -> domain has no dot (no TLD)
  line 22: tel: 020-2555-1234                       -> contains no @ candidate at all

=== final subscriber list: 11 address(es) ===
   1. spandan.andhale@example.com
   2. riya93@mitwpu.edu.in
   3. aman_k99@sub.domain.co.in
   4. name@domain.com
   5. upper.case@example.com
   6. neha+newsletter@gmail.com
   7. sana.shaikh@zoho.in
   8. omkar..patil@example.com
   9. hello_world-123@my-domain.org
  10. feedback@company.co.uk
  11. support@mediverse.in
  duplicates removed: 1

  subscribers written to : d:\Claude- Hospitalisation Services\python-lab-solutions\exp07\data\subscriber_list.txt
  rejections written to  : d:\Claude- Hospitalisation Services\python-lab-solutions\exp07\data\rejected_submissions.txt

=== why the loose pattern is not enough ===
  loose  '[^\s]+@[^\s]+'   matched 18 token(s)
  strict anchored pattern  accepted 12 token(s)
  the strict pattern threw out 6 malformed entries

=== domain breakdown of the subscriber list ===
  example.com            3
  company.co.uk          1
  domain.com             1
  gmail.com              1
  mediverse.in           1
  mitwpu.edu.in          1
  my-domain.org          1
  sub.domain.co.in       1
  zoho.in                1

```

</details>

---

## Experiment 7 - Question 3: Customer Support Logs

Scenario: Customer support logs are saved in support_log.txt and include
complaints together with contact details. Use regex to extract customer email
addresses for follow-up.

Run: python q3_customer_support_logs.py

**File:** [`q3_customer_support_logs.py`](q3_customer_support_logs.py) &nbsp;&middot;&nbsp; **Run:** `python q3_customer_support_logs.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
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
```

</details>

<details>
<summary>Program output</summary>

```text
=== 12 support log line(s) parsed ===

=== parsed tickets ===
  ticket       date        pri  email                                 message
  ----------------------------------------------------------------------------------------------------
  TICKET-4411  2026-11-18  P1   spandan.andhale@example.com           App crashes when I open the bed av
  TICKET-4412  2026-11-18  P3   riya93@mitwpu.edu.in                  Cannot reset my password, the OTP 
  TICKET-4413  2026-11-18  P2   (none found)                          no contact details given, caller r
  TICKET-4414  2026-11-18  P1   aman_k99@sub.domain.co.in             Double charged for the same appoin
  TICKET-4415  2026-11-18  P4   neha.deshmukh+support@gmail.com       Please update my address, reach me
  TICKET-4416  2026-11-18  P2   spandan.andhale@example.com           Follow up on TICKET-4411, still br
  TICKET-4417  2026-11-19  P3   omkar.patil@example.com               Requesting an invoice copy for Oct
  TICKET-4418  2026-11-19  P1   sana.shaikh@zoho.in                   Doctor list shows the wrong depart
  TICKET-4419  2026-11-19  P4   (none found)                          feedback at mediverse dot in (obfu
  TICKET-4420  2026-11-19  P2   riya93@mitwpu.edu.in                  Password reset worked, closing the
  TICKET-4421  2026-11-19  P1   escalation@partnerclinic.co.uk        Patient records failed to sync ove
  TICKET-4422  2026-11-20  P3   aman_k99@sub.domain.co.in             Refund still not credited.

=== contactability ===
  tickets with an email    : 10
  tickets without an email : 2 -> ['TICKET-4413', 'TICKET-4419']

=== 7 unique customer(s) to follow up ===
  spandan.andhale@example.com            2 ticket(s) ['TICKET-4411', 'TICKET-4416'] highest priority P1
  riya93@mitwpu.edu.in                   2 ticket(s) ['TICKET-4412', 'TICKET-4420'] highest priority P2
  aman_k99@sub.domain.co.in              2 ticket(s) ['TICKET-4414', 'TICKET-4422'] highest priority P1
  neha.deshmukh+support@gmail.com        1 ticket(s) ['TICKET-4415'] highest priority P4
  omkar.patil@example.com                1 ticket(s) ['TICKET-4417'] highest priority P3
  sana.shaikh@zoho.in                    1 ticket(s) ['TICKET-4418'] highest priority P1
  escalation@partnerclinic.co.uk         1 ticket(s) ['TICKET-4421'] highest priority P1

=== repeat complainants (2 or more tickets) ===
  spandan.andhale@example.com            2 tickets - call this customer
  riya93@mitwpu.edu.in                   2 tickets - call this customer
  aman_k99@sub.domain.co.in              2 tickets - call this customer

=== P1 escalation list ===
  TICKET-4411  spandan.andhale@example.com            App crashes when I open the bed availabi
  TICKET-4414  aman_k99@sub.domain.co.in              Double charged for the same appointment 
  TICKET-4418  sana.shaikh@zoho.in                    Doctor list shows the wrong department.
  TICKET-4421  escalation@partnerclinic.co.uk         Patient records failed to sync overnight

  follow-up list written to d:\Claude- Hospitalisation Services\python-lab-solutions\exp07\data\followup_emails.txt

=== domain summary ===
  example.com                2
  mitwpu.edu.in              1
  sub.domain.co.in           1
  gmail.com                  1
  zoho.in                    1
  partnerclinic.co.uk        1

```

</details>

---

## Experiment 7 - Question 4: Data Breach Alert System

Scenario: After a data breach, identify leaked email addresses from a
compromised text file (leaked_data.txt). Use regex to extract and list all
unique email addresses for investigation.

Run: python q4_data_breach_alert.py

Note: this is a defensive exercise. The sample file below is synthetic data
written by this script; no real credentials are involved.

**File:** [`q4_data_breach_alert.py`](q4_data_breach_alert.py) &nbsp;&middot;&nbsp; **Run:** `python q4_data_breach_alert.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
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
```

</details>

<details>
<summary>Program output</summary>

```text
=== scanning d:\Claude- Hospitalisation Services\python-lab-solutions\exp07\data\leaked_data.txt ===
  lines   : 15
  bytes   : 909

=== 12 match(es), 10 unique after normalising case ===

=== unique leaked addresses ===
  #   email                                    occurrences           pseudonym
  1   spandan.andhale@example.com                        2    cacb2868c4a1e085
  2   riya93@mitwpu.edu.in                               2    cd45844e4f6b2501
  3   aman_k99@sub.domain.co.in                          1    fc523cacb39cefa3
  4   neha.deshmukh@gmail.com                            1    f0246f01eccf5384
  5   omkar.patil@example.com                            1    3d94241d6d2e9edf
  6   sana.shaikh@zoho.in                                1    9ae18a7d18736e15
  7   admin@mediverse.in                                 1    abf05c431d3f23f4
  8   support@mediverse.in                               1    34fbe294e573c230
  9   billing@partnerclinic.co.uk                        1    a7dd73c46c9e3fc8
  10  ransom.note@darkmail.invalid                       1    2437dd7081be5b0d

=== case-variant duplicates found by normalising ===
  riya93@mitwpu.edu.in                     appeared as ['Riya93@MITWPU.EDU.IN', 'riya93@mitwpu.edu.in']

=== triage ===
  internal/company accounts (2): ['admin@mediverse.in', 'support@mediverse.in']
  external customer accounts (8): 8 addresses
  attacker-supplied address found: ['ransom.note@darkmail.invalid']

=== rows that leaked no address (data quality) ===
  line 2: id,email,password_hash,last_login
  line 9: 7,corrupted-row-no-email,$2b$10$fakehashvalue007,2026-07-01

=== affected domains ===
  example.com                    2 account(s)
  mediverse.in                   2 account(s)  <- internal
  mitwpu.edu.in                  1 account(s)
  sub.domain.co.in               1 account(s)
  gmail.com                      1 account(s)
  zoho.in                        1 account(s)
  partnerclinic.co.uk            1 account(s)
  darkmail.invalid               1 account(s)

  unique list written to : d:\Claude- Hospitalisation Services\python-lab-solutions\exp07\data\breach_unique_emails.txt
  report written to      : d:\Claude- Hospitalisation Services\python-lab-solutions\exp07\data\breach_report.txt

=== recommended next steps ===
  1. force a password reset for all 10 affected accounts
  2. revoke active sessions and API tokens
  3. notify the 8 external users within 72 hours
  4. rotate credentials for the internal accounts first: ['admin@mediverse.in', 'support@mediverse.in']
  5. preserve the original dump as evidence, work on copies only

```

</details>

---

## Experiment 7 - Question 5: Social Media Profile Extractor

Scenario: Public social media profile text may contain email addresses hidden
inside the content. Use regex to extract any found emails and write them to
extracted_emails.txt.

Run: python q5_social_profile_extractor.py

**File:** [`q5_social_profile_extractor.py`](q5_social_profile_extractor.py) &nbsp;&middot;&nbsp; **Run:** `python q5_social_profile_extractor.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
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
```

</details>

<details>
<summary>Program output</summary>

```text
=== 7 profile block(s) scanned ===

=== plain addresses (4) ===
   spandan.andhale@example.com
   aman.backend@gmail.com
   sana.shaikh@zoho.in
   support@mediverse.in

=== de-obfuscated addresses ===
  [[at]/[dot]  ] 'riya [at] designs [dot] studio'                 -> riya@designs.studio
  [(at)/(dot)  ] 'aman_k99 (at) sub.domain (dot) co'              -> aman_k99@sub.domain.co
  [word at/dot ] 'deshmukh at gmail dot com'                      -> deshmukh@gmail.com
  [<at>/<dot>  ] 'omkar <at> example <dot> com'                   -> omkar@example.com

=== per-profile breakdown ===
  @spandan_codes           spandan.andhale@example.com
  @riya_designs            riya@designs.studio
  @aman_backend            aman.backend@gmail.com, aman_k99@sub.domain.co
  @neha_qa                 deshmukh@gmail.com
  @omkar.patil.dev         omkar@example.com
  @sana_devops             sana.shaikh@zoho.in, support@mediverse.in
  @no_contact_user         (no email found)

=== final list: 8 address(es) ===
   1. spandan.andhale@example.com
   2. aman.backend@gmail.com
   3. sana.shaikh@zoho.in
   4. support@mediverse.in
   5. riya@designs.studio
   6. aman_k99@sub.domain.co
   7. deshmukh@gmail.com
   8. omkar@example.com

  written to d:\Claude- Hospitalisation Services\python-lab-solutions\exp07\data\extracted_emails.txt

=== false positives the pattern correctly avoids ===
  @spandan_codes | SY CSE @ MIT-WPU | building MediVerse
  @riya_designs | UI/UX | Pune
  Not an email: 10/10 would recommend @riya_designs
  @aman_backend | Go and Python | ex-intern
  @neha_qa | automation tester
  @omkar.patil.dev | open source
  @sana_devops | k8s | Mumbai
  @no_contact_user | just lurking
  Bio: no email, no DMs, nothing. @ me if you must.
  Price: 50@kg for mangoes <- not an email either

=== note on scraping ===
  These profiles are synthetic text written by this script. A real
  scraper must honour each site's terms of service, robots.txt and
  the applicable data protection rules before collecting contacts.

```

</details>

---

## Experiment 7 - Question 6: Marketing Campaign Contacts

Scenario: The marketing team has a file with scraped text from multiple
websites (web_content.txt). Use regex to scan for email addresses that could
be used for outreach, filtering duplicates.

Run: python q6_marketing_campaign_contacts.py

**File:** [`q6_marketing_campaign_contacts.py`](q6_marketing_campaign_contacts.py) &nbsp;&middot;&nbsp; **Run:** `python q6_marketing_campaign_contacts.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
"""
Experiment 7 - Question 6: Marketing Campaign Contacts

Scenario: The marketing team has a file with scraped text from multiple
websites (web_content.txt). Use regex to scan for email addresses that could
be used for outreach, filtering duplicates.

Run: python q6_marketing_campaign_contacts.py
"""

import os
import re
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
INPUT_FILE = os.path.join(DATA, "web_content.txt")
OUTPUT_FILE = os.path.join(DATA, "campaign_contacts.csv")

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
MAILTO_RE = re.compile(r"mailto:([A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,})",
                       re.I)
SOURCE_RE = re.compile(r"^#\s*source:\s*(\S+)", re.I)

# addresses that are not worth a marketing email
ROLE_PREFIXES = {"noreply", "no-reply", "donotreply", "postmaster",
                 "abuse", "webmaster", "unsubscribe"}

SAMPLE = """# source: https://clinicpune.example.com/contact
<a href="mailto:frontdesk@clinicpune.example.com">Front desk</a>
Call 020-2555-1234 or write to admin@clinicpune.example.com
Do not reply to noreply@clinicpune.example.com

# source: https://medsupplies.example.in/about
Procurement: purchase@medsupplies.example.in
Sales head: r.mehta@medsupplies.example.in
Careers: hr@medsupplies.example.in
Footer: (c) 2026 MedSupplies. unsubscribe@medsupplies.example.in

# source: https://healthblog.example.org/post/12
Written by Dr. Kavita Rao - kavita.rao@healthblog.example.org
Guest post enquiries: editor@healthblog.example.org
Our earlier article mentioned admin@clinicpune.example.com as a partner.

# source: https://diagnostics.example.net/team
Lab head: s.iyer@diagnostics.example.net
Reception: reception@diagnostics.example.net
Webmaster: webmaster@diagnostics.example.net
Press: PRESS@Diagnostics.Example.NET

# source: https://pharmachain.example.co/contact
<a href="mailto:b2b@pharmachain.example.co?subject=Bulk">B2B orders</a>
Store locator has no email. Phone 1800-123-456.
Franchise: franchise@pharmachain.example.co
Duplicate listing: b2b@pharmachain.example.co
"""


def ensure_sample():
    os.makedirs(DATA, exist_ok=True)
    if not os.path.exists(INPUT_FILE):
        with open(INPUT_FILE, "w", encoding="utf-8") as fh:
            fh.write(SAMPLE)
        print(f"[setup] created sample input {INPUT_FILE}")


def is_role_account(email):
    return email.split("@")[0].lower() in ROLE_PREFIXES


if __name__ == "__main__":
    ensure_sample()

    with open(INPUT_FILE, "r", encoding="utf-8") as fh:
        lines = fh.read().splitlines()

    # walk the file, remembering which source block we are inside
    hits = []           # (email, source)
    current_source = "(unknown)"
    for line in lines:
        m = SOURCE_RE.match(line)
        if m:
            current_source = m.group(1)
            continue
        for email in EMAIL_RE.findall(line):
            hits.append((email.lower(), current_source))

    mailto_hits = [m.lower() for m in MAILTO_RE.findall("\n".join(lines))]

    sources = sorted({s for _, s in hits})
    print(f"=== scanned {len(lines)} line(s) from {len(sources)} website(s) ===")
    for s in sources:
        print("  ", s)

    print(f"\n=== {len(hits)} raw match(es) ===")
    print(f"  of which {len(mailto_hits)} came from mailto: links -> "
          f"{mailto_hits}")

    counts = Counter(e for e, _ in hits)
    duplicates = {e: c for e, c in counts.items() if c > 1}

    unique = []
    seen_sources = defaultdict(set)
    for email, source in hits:
        seen_sources[email].add(source)
        if email not in unique:
            unique.append(email)

    print(f"\n=== duplicate filter ===")
    print(f"  raw matches     : {len(hits)}")
    print(f"  unique addresses: {len(unique)}")
    print(f"  duplicates found: {len(hits) - len(unique)}")
    for email, c in sorted(duplicates.items(), key=lambda kv: -kv[1]):
        print(f"    {email:<44} appeared {c} time(s) across "
              f"{len(seen_sources[email])} site(s)")

    usable = [e for e in unique if not is_role_account(e)]
    skipped = [e for e in unique if is_role_account(e)]

    print(f"\n=== outreach suitability ===")
    print(f"  usable contacts     : {len(usable)}")
    print(f"  role/no-reply boxes : {len(skipped)} -> {skipped}")

    print(f"\n=== final campaign list ===")
    print(f"  {'email':<48}{'domain':<34}sources")
    print("  " + "-" * 96)
    for e in usable:
        domain = e.split("@")[1]
        srcs = ", ".join(sorted(seen_sources[e]))
        print(f"  {e:<48}{domain:<34}{srcs[:40]}")

    print("\n=== grouped by company domain ===")
    by_domain = defaultdict(list)
    for e in usable:
        by_domain[e.split("@")[1]].append(e)
    for domain, members in sorted(by_domain.items()):
        print(f"  {domain:<36} {len(members)} contact(s)")
        for m in members:
            print(f"      {m}")

    with open(OUTPUT_FILE, "w", encoding="utf-8", newline="") as fh:
        fh.write("email,domain,times_seen,sources\n")
        for e in usable:
            srcs = ";".join(sorted(seen_sources[e]))
            fh.write(f"{e},{e.split('@')[1]},{counts[e]},{srcs}\n")
    print(f"\n  campaign list written to {OUTPUT_FILE}")

    print("\n=== compliance reminder for the marketing team ===")
    print("  Scraped addresses are not consent. Before sending, confirm a")
    print("  lawful basis, include an unsubscribe link, and honour opt-outs.")
    print(f"  {len(skipped)} no-reply/role box(es) were removed automatically.")
```

</details>

<details>
<summary>Program output</summary>

```text
=== scanned 27 line(s) from 5 website(s) ===
   https://clinicpune.example.com/contact
   https://diagnostics.example.net/team
   https://healthblog.example.org/post/12
   https://medsupplies.example.in/about
   https://pharmachain.example.co/contact

=== 17 raw match(es) ===
  of which 2 came from mailto: links -> ['frontdesk@clinicpune.example.com', 'b2b@pharmachain.example.co']

=== duplicate filter ===
  raw matches     : 17
  unique addresses: 15
  duplicates found: 2
    admin@clinicpune.example.com                 appeared 2 time(s) across 2 site(s)
    b2b@pharmachain.example.co                   appeared 2 time(s) across 1 site(s)

=== outreach suitability ===
  usable contacts     : 12
  role/no-reply boxes : 3 -> ['noreply@clinicpune.example.com', 'unsubscribe@medsupplies.example.in', 'webmaster@diagnostics.example.net']

=== final campaign list ===
  email                                           domain                            sources
  ------------------------------------------------------------------------------------------------
  frontdesk@clinicpune.example.com                clinicpune.example.com            https://clinicpune.example.com/contact
  admin@clinicpune.example.com                    clinicpune.example.com            https://clinicpune.example.com/contact, 
  purchase@medsupplies.example.in                 medsupplies.example.in            https://medsupplies.example.in/about
  r.mehta@medsupplies.example.in                  medsupplies.example.in            https://medsupplies.example.in/about
  hr@medsupplies.example.in                       medsupplies.example.in            https://medsupplies.example.in/about
  kavita.rao@healthblog.example.org               healthblog.example.org            https://healthblog.example.org/post/12
  editor@healthblog.example.org                   healthblog.example.org            https://healthblog.example.org/post/12
  s.iyer@diagnostics.example.net                  diagnostics.example.net           https://diagnostics.example.net/team
  reception@diagnostics.example.net               diagnostics.example.net           https://diagnostics.example.net/team
  press@diagnostics.example.net                   diagnostics.example.net           https://diagnostics.example.net/team
  b2b@pharmachain.example.co                      pharmachain.example.co            https://pharmachain.example.co/contact
  franchise@pharmachain.example.co                pharmachain.example.co            https://pharmachain.example.co/contact

=== grouped by company domain ===
  clinicpune.example.com               2 contact(s)
      frontdesk@clinicpune.example.com
      admin@clinicpune.example.com
  diagnostics.example.net              3 contact(s)
      s.iyer@diagnostics.example.net
      reception@diagnostics.example.net
      press@diagnostics.example.net
  healthblog.example.org               2 contact(s)
      kavita.rao@healthblog.example.org
      editor@healthblog.example.org
  medsupplies.example.in               3 contact(s)
      purchase@medsupplies.example.in
      r.mehta@medsupplies.example.in
      hr@medsupplies.example.in
  pharmachain.example.co               2 contact(s)
      b2b@pharmachain.example.co
      franchise@pharmachain.example.co

  campaign list written to d:\Claude- Hospitalisation Services\python-lab-solutions\exp07\data\campaign_contacts.csv

=== compliance reminder for the marketing team ===
  Scraped addresses are not consent. Before sending, confirm a
  lawful basis, include an unsubscribe link, and honour opt-outs.
  3 no-reply/role box(es) were removed automatically.

```

</details>

---

## Experiment 7 - Question 7: Classroom Group Project Submissions

Scenario: Students submit group project reports listing their names and
emails. Use regex to extract the email addresses from group_reports.txt for
grade distribution.

Run: python q7_group_project_submissions.py

**File:** [`q7_group_project_submissions.py`](q7_group_project_submissions.py) &nbsp;&middot;&nbsp; **Run:** `python q7_group_project_submissions.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
"""
Experiment 7 - Question 7: Classroom Group Project Submissions

Scenario: Students submit group project reports listing their names and
emails. Use regex to extract the email addresses from group_reports.txt for
grade distribution.

Run: python q7_group_project_submissions.py
"""

import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
INPUT_FILE = os.path.join(DATA, "group_reports.txt")
OUTPUT_FILE = os.path.join(DATA, "grade_distribution_list.txt")

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
GROUP_RE = re.compile(r"^Group\s+(\d+)\s*[-:]\s*(.+)$", re.I)
MEMBER_RE = re.compile(
    r"^\s*(?:\d+[.)]\s*)?(?P<name>[A-Z][A-Za-z.\s]+?)\s*[-,(<]?\s*"
    r"(?P<roll>[A-Z]{2,4}\d{4})?\s*[-,(<]?\s*"
    r"(?P<email>[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,})"
)
COLLEGE_DOMAIN = "mitwpu.edu.in"

SAMPLE = """Group 1 - MediVerse: Hospital Services Portal
1. Spandan Andhale CSE2301 spandan.andhale@mitwpu.edu.in
2. Riya Sharma CSE2302 riya.sharma@mitwpu.edu.in
3. Aman Kulkarni CSE2303 aman.kulkarni@mitwpu.edu.in
Guide: Prof. S. Joshi s.joshi@mitwpu.edu.in

Group 2 - Smart Attendance using Face Recognition
1. Neha Deshmukh CSE2311 neha.deshmukh@mitwpu.edu.in
2. Omkar Patil CSE2312 omkar.patil@mitwpu.edu.in
3. Sana Shaikh CSE2313 sana.shaikh99@gmail.com
Note: Sana's college mail is blocked, personal id given.

Group 3 - Crop Yield Prediction
1. Rohit Jadhav CSE2321 rohit.jadhav@mitwpu.edu.in
2. Pooja Nair CSE2322 pooja.nair@mitwpu.edu.in
3. Kiran Rao CSE2323 (email not submitted)

Group 4 - Library Management System
1. Tanvi Gokhale CSE2331 tanvi.gokhale@mitwpu.edu.in
2. Harsh Mehta CSE2332 harsh.mehta@mitwpu.edu.in
3. Spandan Andhale CSE2301 spandan.andhale@mitwpu.edu.in
Note: Spandan contributed to two groups this semester.
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

    groups = []
    current = None
    for line in lines:
        gm = GROUP_RE.match(line)
        if gm:
            current = {"number": int(gm.group(1)), "title": gm.group(2).strip(),
                       "members": [], "guide": None, "notes": []}
            groups.append(current)
            continue
        if current is None:
            continue
        if line.lower().startswith("guide"):
            found = EMAIL_RE.findall(line)
            current["guide"] = found[0].lower() if found else None
            continue
        if line.lower().startswith("note"):
            current["notes"].append(line.strip())
            continue
        mm = MEMBER_RE.match(line)
        if mm:
            current["members"].append({
                "name": mm.group("name").strip(),
                "roll": mm.group("roll"),
                "email": mm.group("email").lower(),
            })
        elif line.strip() and EMAIL_RE.search(line):
            current["members"].append({
                "name": "(name not parsed)", "roll": None,
                "email": EMAIL_RE.search(line).group(0).lower()})
        elif line.strip() and "email not submitted" in line.lower():
            current["members"].append({
                "name": line.split("CSE")[0].strip().lstrip("123. "),
                "roll": (re.search(r"CSE\d{4}", line).group(0)
                         if re.search(r"CSE\d{4}", line) else None),
                "email": None})

    print(f"=== {len(groups)} group(s) parsed from {os.path.basename(INPUT_FILE)}"
          f" ===")

    all_emails = []
    for g in groups:
        print(f"\n  Group {g['number']}: {g['title']}")
        for m in g["members"]:
            email = m["email"] or "(MISSING)"
            print(f"    {m['name']:<18}{str(m['roll'] or '-'):<10}{email}")
            if m["email"]:
                all_emails.append(m["email"])
        if g["guide"]:
            print(f"    {'Guide':<18}{'-':<10}{g['guide']}")
        for note in g["notes"]:
            print(f"    note: {note}")

    unique_students = []
    for e in all_emails:
        if e not in unique_students:
            unique_students.append(e)

    print(f"\n=== extraction summary ===")
    print(f"  member email matches : {len(all_emails)}")
    print(f"  unique students      : {len(unique_students)}")
    print(f"  duplicates (students in two groups): "
          f"{len(all_emails) - len(unique_students)}")

    missing = [(g["number"], m["name"]) for g in groups for m in g["members"]
               if not m["email"]]
    print(f"  members without an email: {len(missing)} -> {missing}")

    college = [e for e in unique_students if e.endswith(COLLEGE_DOMAIN)]
    personal = [e for e in unique_students if not e.endswith(COLLEGE_DOMAIN)]
    print(f"\n=== domain check (college policy) ===")
    print(f"  college addresses  : {len(college)}")
    print(f"  personal addresses : {len(personal)} -> {personal}")
    if personal:
        print("  action: ask these students to register their college id")

    print("\n=== duplicate participation ===")
    for e in unique_students:
        in_groups = [g["number"] for g in groups
                     if any(m["email"] == e for m in g["members"])]
        if len(in_groups) > 1:
            print(f"  {e} appears in groups {in_groups}")

    guides = [g["guide"] for g in groups if g["guide"]]
    unique_guides = sorted(set(guides))
    print(f"\n=== guides ({len(unique_guides)}) ===")
    for g in unique_guides:
        print("  ", g)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as fh:
        fh.write("# grade distribution list\n")
        for g in groups:
            fh.write(f"\nGroup {g['number']}: {g['title']}\n")
            for m in g["members"]:
                if m["email"]:
                    fh.write(f"  {m['email']}\n")
        fh.write("\n# guides\n")
        for g in unique_guides:
            fh.write(f"  {g}\n")
        fh.write(f"\n# all unique student addresses ({len(unique_students)})\n")
        fh.write("; ".join(unique_students) + "\n")

    print(f"\n  grade distribution list written to {OUTPUT_FILE}")
    print(f"\n=== ready-to-paste BCC line ===")
    print("  " + "; ".join(unique_students))
```

</details>

<details>
<summary>Program output</summary>

```text
=== 4 group(s) parsed from group_reports.txt ===

  Group 1: MediVerse: Hospital Services Portal
    Spandan Andhale   CSE2301   spandan.andhale@mitwpu.edu.in
    Riya Sharma       CSE2302   riya.sharma@mitwpu.edu.in
    Aman Kulkarni     CSE2303   aman.kulkarni@mitwpu.edu.in
    Guide             -         s.joshi@mitwpu.edu.in

  Group 2: Smart Attendance using Face Recognition
    Neha Deshmukh     CSE2311   neha.deshmukh@mitwpu.edu.in
    Omkar Patil       CSE2312   omkar.patil@mitwpu.edu.in
    Sana Shaikh       CSE2313   sana.shaikh99@gmail.com
    note: Note: Sana's college mail is blocked, personal id given.

  Group 3: Crop Yield Prediction
    Rohit Jadhav      CSE2321   rohit.jadhav@mitwpu.edu.in
    Pooja Nair        CSE2322   pooja.nair@mitwpu.edu.in
    Kiran Rao         CSE2323   (MISSING)

  Group 4: Library Management System
    Tanvi Gokhale     CSE2331   tanvi.gokhale@mitwpu.edu.in
    Harsh Mehta       CSE2332   harsh.mehta@mitwpu.edu.in
    Spandan Andhale   CSE2301   spandan.andhale@mitwpu.edu.in
    note: Note: Spandan contributed to two groups this semester.

=== extraction summary ===
  member email matches : 11
  unique students      : 10
  duplicates (students in two groups): 1
  members without an email: 1 -> [(3, 'Kiran Rao')]

=== domain check (college policy) ===
  college addresses  : 9
  personal addresses : 1 -> ['sana.shaikh99@gmail.com']
  action: ask these students to register their college id

=== duplicate participation ===
  spandan.andhale@mitwpu.edu.in appears in groups [1, 4]

=== guides (1) ===
   s.joshi@mitwpu.edu.in

  grade distribution list written to d:\Claude- Hospitalisation Services\python-lab-solutions\exp07\data\grade_distribution_list.txt

=== ready-to-paste BCC line ===
  spandan.andhale@mitwpu.edu.in; riya.sharma@mitwpu.edu.in; aman.kulkarni@mitwpu.edu.in; neha.deshmukh@mitwpu.edu.in; omkar.patil@mitwpu.edu.in; sana.shaikh99@gmail.com; rohit.jadhav@mitwpu.edu.in; pooja.nair@mitwpu.edu.in; tanvi.gokhale@mitwpu.edu.in; harsh.mehta@mitwpu.edu.in

```

</details>

---

## Experiment 7 - Question 8: Event Registration Email Filter

Scenario: An event registration form allows free text and the entries are
saved in registration_entries.txt. Use regex to find and validate the entered
email addresses for sending event details.

Run: python q8_event_registration_filter.py

**File:** [`q8_event_registration_filter.py`](q8_event_registration_filter.py) &nbsp;&middot;&nbsp; **Run:** `python q8_event_registration_filter.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
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
```

</details>

<details>
<summary>Program output</summary>

```text
=== 15 registration entry(ies) ===

=== 10 valid address(es) ===
  REG-001   spandan.andhale@example.com
  REG-002   riya93@mitwpu.edu.in
  REG-003   aman_k99@gmial.com
  REG-004   neha.deshmukh@gmail.com
  REG-006   sana.shaikh@zoho.in
  REG-008   pooja..nair@example.com
  REG-009   kiran.rao@diagnostics.example.net
  REG-010   tanvi.gokhale@mitwpu.edu.in
  REG-013   spandan.andhale@example.com
  REG-014   kavita.rao@healthblog.example.org

=== 5 entry(ies) needing correction ===
  id       as typed                        problem                     suggestion
  --------------------------------------------------------------------------------------------
  REG-005  (none)                          no email in the entry       -
  REG-007  (none)                          no email in the entry       -
  REG-011  harsh@mehta@example.com         more than one @             -
  REG-012  (none)                          no email in the entry       -
  REG-015  sameer@short.c                  top level domain too short  -

=== final mailing list: 9 recipient(s) ===
   1. spandan.andhale@example.com  (registered 2 times)
   2. riya93@mitwpu.edu.in
   3. aman_k99@gmial.com
   4. neha.deshmukh@gmail.com
   5. sana.shaikh@zoho.in
   6. pooja..nair@example.com
   7. kiran.rao@diagnostics.example.net
   8. tanvi.gokhale@mitwpu.edu.in
   9. kavita.rao@healthblog.example.org
  duplicate registrations removed: 1

=== registration statistics ===
  entries submitted      : 15
  contactable attendees  : 9
  entries to chase up    : 5
  data quality           : 60.0% usable
  auto-fixable typos     : 0

=== attendee domains ===
  example.com                        2
  mitwpu.edu.in                      2
  gmial.com                          1
  gmail.com                          1
  zoho.in                            1
  diagnostics.example.net            1
  healthblog.example.org             1

  mailing list written to : d:\Claude- Hospitalisation Services\python-lab-solutions\exp07\data\event_mailing_list.txt
  corrections written to  : d:\Claude- Hospitalisation Services\python-lab-solutions\exp07\data\entries_needing_correction.txt

```

</details>

---

## Experiment 7 - Question 9: Resume Parser Tool

Scenario: Build a resume parser that extracts key information, including email
addresses, from resumes saved as .txt. Use regex to pull out candidate emails
for recruiter review.

Run: python q9_resume_parser.py

**File:** [`q9_resume_parser.py`](q9_resume_parser.py) &nbsp;&middot;&nbsp; **Run:** `python q9_resume_parser.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
"""
Experiment 7 - Question 9: Resume Parser Tool

Scenario: Build a resume parser that extracts key information, including email
addresses, from resumes saved as .txt. Use regex to pull out candidate emails
for recruiter review.

Run: python q9_resume_parser.py
"""

import os
import re
import json

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
RESUME_DIR = os.path.join(DATA, "resumes")
OUTPUT_FILE = os.path.join(DATA, "parsed_candidates.json")

PATTERNS = {
    "email": re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}"),
    "phone": re.compile(r"(?:\+91[\s\-]?)?\b\d{5}[\s\-]?\d{5}\b"
                        r"|\b0\d{2,4}[\s\-]\d{6,8}\b"),
    "linkedin": re.compile(r"(?:https?://)?(?:www\.)?linkedin\.com/in/[\w\-]+",
                           re.I),
    "github": re.compile(r"(?:https?://)?(?:www\.)?github\.com/[\w\-]+", re.I),
    "cgpa": re.compile(r"\b(?:CGPA|GPA)\s*[:\-]?\s*(\d\.\d{1,2})\b", re.I),
    "year": re.compile(r"\b(19|20)\d{2}\b"),
}
SKILL_LINE = re.compile(r"^\s*(?:Skills|Technical Skills|Tech Stack)\s*[:\-]\s*(.+)$",
                        re.I | re.M)
NAME_RE = re.compile(r"^([A-Z][a-z]+(?:\s+[A-Z][a-z.]+){1,3})\s*$", re.M)

RESUMES = {
    "spandan_andhale.txt": """Spandan Andhale
Pune, Maharashtra | +91 90112 23344 | spandan.andhale@example.com
linkedin.com/in/spandan-andhale | github.com/spandanandhale2007-max

EDUCATION
MIT World Peace University, Pune - B.Tech Computer Science, 2024-2028
CGPA: 8.74

Skills: Python, JavaScript, React, Vite, Supabase, Git, SQL

PROJECTS
MediVerse - hospital services portal with bed availability and appointments.
Built with React and Python, deployed on Netlify.
""",
    "riya_sharma.txt": """Riya Sharma
riya93@mitwpu.edu.in / personal: riya.sharma.design@gmail.com
Phone: 98765 43210
Portfolio: behance.net/riyasharma

EDUCATION
MIT-WPU, B.Des Interaction Design, 2023-2027. GPA: 9.1

Technical Skills: Figma, Adobe XD, HTML, CSS, Framer Motion
""",
    "aman_kulkarni.txt": """Aman Kulkarni
Contact: aman_k99@sub.domain.co.in
Mobile 020-2555 1234
github.com/amank99

EDUCATION
Savitribai Phule Pune University, MCA, 2022-2024, CGPA 7.9

Tech Stack: Go, Python, Docker, Kubernetes, PostgreSQL
""",
    "no_contact.txt": """Kiran Rao
Pune

EDUCATION
B.Sc Statistics, 2021

Skills: R, Excel, SPSS

(No email or phone number listed on this resume.)
""",
}


def ensure_samples():
    os.makedirs(RESUME_DIR, exist_ok=True)
    created = 0
    for name, body in RESUMES.items():
        path = os.path.join(RESUME_DIR, name)
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(body)
            created += 1
    if created:
        print(f"[setup] created {created} sample resume(s) in {RESUME_DIR}")


def parse_resume(path):
    with open(path, "r", encoding="utf-8") as fh:
        text = fh.read()

    emails = [e.lower() for e in PATTERNS["email"].findall(text)]
    unique_emails = []
    for e in emails:
        if e not in unique_emails:
            unique_emails.append(e)

    name_match = NAME_RE.search(text)
    skills_match = SKILL_LINE.search(text)
    cgpa_match = PATTERNS["cgpa"].search(text)

    return {
        "file": os.path.basename(path),
        "name": name_match.group(1) if name_match else "(not detected)",
        "emails": unique_emails,
        "primary_email": unique_emails[0] if unique_emails else None,
        "phones": PATTERNS["phone"].findall(text),
        "linkedin": PATTERNS["linkedin"].findall(text),
        "github": PATTERNS["github"].findall(text),
        "cgpa": float(cgpa_match.group(1)) if cgpa_match else None,
        "skills": [s.strip() for s in skills_match.group(1).split(",")]
                  if skills_match else [],
        "words": len(text.split()),
    }


if __name__ == "__main__":
    ensure_samples()

    files = sorted(f for f in os.listdir(RESUME_DIR) if f.endswith(".txt"))
    print(f"=== parsing {len(files)} resume(s) ===")

    candidates = [parse_resume(os.path.join(RESUME_DIR, f)) for f in files]

    for c in candidates:
        print(f"\n  --- {c['file']} ---")
        print(f"  name     : {c['name']}")
        print(f"  email(s) : {', '.join(c['emails']) or '(NONE FOUND)'}")
        print(f"  phone(s) : {', '.join(c['phones']) or '-'}")
        print(f"  linkedin : {', '.join(c['linkedin']) or '-'}")
        print(f"  github   : {', '.join(c['github']) or '-'}")
        print(f"  cgpa     : {c['cgpa'] if c['cgpa'] is not None else '-'}")
        print(f"  skills   : {', '.join(c['skills']) or '-'}")
        print(f"  length   : {c['words']} words")

    print("\n=== recruiter email list ===")
    contactable = [c for c in candidates if c["primary_email"]]
    for c in contactable:
        print(f"  {c['name']:<20}{c['primary_email']}")
    missing = [c["file"] for c in candidates if not c["primary_email"]]
    print(f"\n  contactable : {len(contactable)}/{len(candidates)}")
    if missing:
        print(f"  no email    : {missing} - request contact details")

    print("\n=== candidates with more than one address ===")
    for c in candidates:
        if len(c["emails"]) > 1:
            print(f"  {c['name']:<20}{c['emails']}  "
                  f"(use the first, {c['primary_email']})")

    print("\n=== shortlist: CGPA 8.0 or above with an email ===")
    shortlist = [c for c in contactable
                 if c["cgpa"] is not None and c["cgpa"] >= 8.0]
    for c in sorted(shortlist, key=lambda x: -x["cgpa"]):
        print(f"  {c['name']:<20}CGPA {c['cgpa']:<6}{c['primary_email']}")
    if not shortlist:
        print("  none met the cut-off")

    print("\n=== skill index ===")
    index = {}
    for c in candidates:
        for s in c["skills"]:
            index.setdefault(s, []).append(c["name"])
    for skill, names in sorted(index.items()):
        print(f"  {skill:<18}{', '.join(names)}")

    print("\n=== Python developers to contact ===")
    for c in contactable:
        if any(s.lower() == "python" for s in c["skills"]):
            print(f"  {c['primary_email']:<40}{c['name']}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as fh:
        json.dump(candidates, fh, indent=2)
    print(f"\n  structured output written to {OUTPUT_FILE}")

    print("\n=== BCC line for the interview invite ===")
    print("  " + "; ".join(c["primary_email"] for c in contactable))
```

</details>

<details>
<summary>Program output</summary>

```text
=== parsing 4 resume(s) ===

  --- aman_kulkarni.txt ---
  name     : Aman Kulkarni
  email(s) : aman_k99@sub.domain.co.in
  phone(s) : -
  linkedin : -
  github   : github.com/amank99
  cgpa     : 7.9
  skills   : Go, Python, Docker, Kubernetes, PostgreSQL
  length   : 24 words

  --- no_contact.txt ---
  name     : Kiran Rao
Pune
  email(s) : (NONE FOUND)
  phone(s) : -
  linkedin : -
  github   : -
  cgpa     : -
  skills   : R, Excel, SPSS
  length   : 20 words

  --- riya_sharma.txt ---
  name     : Riya Sharma
  email(s) : riya93@mitwpu.edu.in, riya.sharma.design@gmail.com
  phone(s) : 98765 43210
  linkedin : -
  github   : -
  cgpa     : 9.1
  skills   : Figma, Adobe XD, HTML, CSS, Framer Motion
  length   : 28 words

  --- spandan_andhale.txt ---
  name     : Spandan Andhale
  email(s) : spandan.andhale@example.com
  phone(s) : +91 90112 23344
  linkedin : linkedin.com/in/spandan-andhale
  github   : github.com/spandanandhale2007-max
  cgpa     : 8.74
  skills   : Python, JavaScript, React, Vite, Supabase, Git, SQL
  length   : 53 words

=== recruiter email list ===
  Aman Kulkarni       aman_k99@sub.domain.co.in
  Riya Sharma         riya93@mitwpu.edu.in
  Spandan Andhale     spandan.andhale@example.com

  contactable : 3/4
  no email    : ['no_contact.txt'] - request contact details

=== candidates with more than one address ===
  Riya Sharma         ['riya93@mitwpu.edu.in', 'riya.sharma.design@gmail.com']  (use the first, riya93@mitwpu.edu.in)

=== shortlist: CGPA 8.0 or above with an email ===
  Riya Sharma         CGPA 9.1   riya93@mitwpu.edu.in
  Spandan Andhale     CGPA 8.74  spandan.andhale@example.com

=== skill index ===
  Adobe XD          Riya Sharma
  CSS               Riya Sharma
  Docker            Aman Kulkarni
  Excel             Kiran Rao
Pune
  Figma             Riya Sharma
  Framer Motion     Riya Sharma
  Git               Spandan Andhale
  Go                Aman Kulkarni
  HTML              Riya Sharma
  JavaScript        Spandan Andhale
  Kubernetes        Aman Kulkarni
  PostgreSQL        Aman Kulkarni
  Python            Aman Kulkarni, Spandan Andhale
  R                 Kiran Rao
Pune
  React             Spandan Andhale
  SPSS              Kiran Rao
Pune
  SQL               Spandan Andhale
  Supabase          Spandan Andhale
  Vite              Spandan Andhale

=== Python developers to contact ===
  aman_k99@sub.domain.co.in               Aman Kulkarni
  spandan.andhale@example.com             Spandan Andhale

  structured output written to d:\Claude- Hospitalisation Services\python-lab-solutions\exp07\data\parsed_candidates.json

=== BCC line for the interview invite ===
  aman_k99@sub.domain.co.in; riya93@mitwpu.edu.in; spandan.andhale@example.com

```

</details>

---

## Experiment 7 - Question 10: Spam Detector System

Scenario: Analyse potentially spammy content from user messages
(spam_check.txt). Use regex to find and flag messages that include suspicious
email addresses for further inspection.

Run: python q10_spam_detector.py

**File:** [`q10_spam_detector.py`](q10_spam_detector.py) &nbsp;&middot;&nbsp; **Run:** `python q10_spam_detector.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
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
```

</details>

<details>
<summary>Program output</summary>

```text
=== 12 message(s) to inspect ===

=== verdicts ===
  id       sender                                   email  body  score  verdict
  ------------------------------------------------------------------------------
  MSG-001  spandan.andhale@example.com                  0     0      0  CLEAN
  MSG-002  winner27381@mailinator.com                   4     5      9  SPAM
  MSG-003  riya93@mitwpu.edu.in                         0     0      0  CLEAN
  MSG-004  support@mediverse.in                         0     0      0  CLEAN
  MSG-005  crypto.doubler@gains.top                     3     3      6  SPAM
  MSG-006  aman_k99@sub.domain.co.in                    0     0      0  CLEAN
  MSG-007  security-alert@mediverse-in.xyz              6     3      9  SPAM
  MSG-008  a9f83kd92jdk19dkq@throwaway.email            6     1      7  SPAM
  MSG-009  neha.deshmukh@gmail.com                      0     0      0  CLEAN
  MSG-010  hr@medsupplies.example.in                    0     0      0  CLEAN
  MSG-011  no-reply@ransom.note.invalid                 3     1      4  SUSPECT
  MSG-012  kavita.rao@healthblog.example.org            0     0      0  CLEAN

=== flagged messages in detail ===

  MSG-002 [SPAM, score 9]
    sender : winner27381@mailinator.com
    body   : CONGRATULATIONS!! You are our lottery WINNER. Claim your prize now, cl
    address flags : disposable mail provider, many digits in the local part
    content flags : winner, lottery, click here, prize, multiple exclamation marks

  MSG-005 [SPAM, score 6]
    sender : crypto.doubler@gains.top
    body   : Double your money in 24 hours. Send BTC to this wallet. ACT NOW, limit
    address flags : suspicious TLD .top
    content flags : double your, act now, limited offer

  MSG-007 [SPAM, score 9]
    sender : security-alert@mediverse-in.xyz
    body   : URGENT: verify your account or it will be closed. Reply with your bank
    address flags : suspicious TLD .xyz, look-alike domain impersonating a brand
    content flags : urgent, verify your account, bank details

  MSG-008 [SPAM, score 7]
    sender : a9f83kd92jdk19dkq@throwaway.email
    body   : free money free money free money
    address flags : disposable mail provider, machine-generated local part, many digits in the local part
    content flags : free money

  MSG-011 [SUSPECT, score 4]
    sender : no-reply@ransom.note.invalid
    body   : We have your records. Wire transfer 2 BTC or we publish them.
    address flags : suspicious TLD .invalid
    content flags : wire transfer

=== summary ===
  SPAM       4 message(s)
  SUSPECT    1 message(s)
  CLEAN      7 message(s)
  spam rate: 33.3%

=== sender domains by verdict ===
  SPAM     ['gains.top', 'mailinator.com', 'mediverse-in.xyz', 'throwaway.email']
  SUSPECT  ['ransom.note.invalid']
  CLEAN    ['example.com', 'gmail.com', 'healthblog.example.org', 'mediverse.in', 'medsupplies.example.in', 'mitwpu.edu.in', 'sub.domain.co.in']

=== blocklist suggestion ===
  block domain: gains.top
  block domain: mailinator.com
  block domain: mediverse-in.xyz
  block domain: throwaway.email

  flagged messages written to d:\Claude- Hospitalisation Services\python-lab-solutions\exp07\data\flagged_messages.txt

=== note ===
  This is a rule-based filter for a lab exercise. Real spam
  filtering combines such signals with sender reputation, SPF,
  DKIM and DMARC checks, and a trained classifier.

```

</details>

---
