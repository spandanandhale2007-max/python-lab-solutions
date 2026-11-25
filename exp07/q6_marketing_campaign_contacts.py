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
