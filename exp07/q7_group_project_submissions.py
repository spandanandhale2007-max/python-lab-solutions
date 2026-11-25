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
