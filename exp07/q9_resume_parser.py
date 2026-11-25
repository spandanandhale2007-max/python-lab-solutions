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
