"""
Experiment 9 - Question 9: Student Records Management System

Scenario: A school stores student details in students.csv with fields such as
student_id, name, grade and email. Convert the CSV into students.json to
integrate with a web-based student portal.

Usage:
  python q9_students_csv_to_json.py
  python q9_students_csv_to_json.py --group-by-grade
"""

import argparse
import csv
import json
import os
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
DEFAULT_CSV = os.path.join(DATA, "students.csv")
DEFAULT_JSON = os.path.join(DATA, "students.json")

SAMPLE_CSV = """student_id,name,grade,email,section,attendance_percent
STU-2301,Spandan Andhale,SY-CSE,spandan.andhale@school.edu.in,A,92.5
STU-2302,Riya Sharma,SY-CSE,riya.sharma@school.edu.in,A,88.0
STU-2303,Aman Kulkarni,SY-CSE,aman.kulkarni@school.edu.in,B,74.5
STU-2304,Neha Deshmukh,TY-CSE,neha.deshmukh@school.edu.in,A,96.0
STU-2305,Omkar Patil,TY-CSE,omkar.patil@school.edu.in,B,61.5
STU-2306,Sana Shaikh,FY-CSE,sana.shaikh@school.edu.in,A,85.0
STU-2307,Rohit Jadhav,FY-CSE,rohit.jadhav@school.edu.in,B,79.0
STU-2308,Pooja Nair,SY-CSE,pooja.nair@school.edu.in,B,58.0
STU-2309,Kiran Rao,TY-CSE,kiran.rao@school.edu.in,A,90.5
STU-2310,Tanvi Gokhale,FY-CSE,tanvi.gokhale@school.edu.in,A,99.0
"""

ATTENDANCE_CUTOFF = 75.0


def ensure_sample(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8", newline="") as fh:
            fh.write(SAMPLE_CSV)
        print(f"[setup] created sample input {path}")


def to_record(row):
    attendance = float(row["attendance_percent"])
    return {
        "studentId": row["student_id"],
        "name": row["name"],
        "grade": row["grade"],
        "email": row["email"].lower(),
        "section": row["section"],
        "attendancePercent": attendance,
        "attendanceOk": attendance >= ATTENDANCE_CUTOFF,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert a student records CSV into portal-ready JSON.")
    parser.add_argument("--input", default=DEFAULT_CSV)
    parser.add_argument("--output", default=DEFAULT_JSON)
    parser.add_argument("--indent", type=int, default=2)
    parser.add_argument("--group-by-grade", action="store_true",
                        help="nest the records under each grade")
    args = parser.parse_args()

    ensure_sample(args.input)

    with open(args.input, "r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)
        headers = reader.fieldnames

    print(f"=== read {os.path.basename(args.input)} ===")
    print(f"  columns  : {headers}")
    print(f"  students : {len(rows)}")
    print(f"  size     : {os.path.getsize(args.input)} bytes")

    print("\n=== CSV contents ===")
    print(f"  {'id':<10}{'name':<18}{'grade':<9}{'sec':<5}"
          f"{'attendance':>11}  email")
    print("  " + "-" * 92)
    for r in rows:
        print(f"  {r['student_id']:<10}{r['name']:<18}{r['grade']:<9}"
              f"{r['section']:<5}{r['attendance_percent']:>10}%  {r['email']}")

    print("\n=== validation ===")
    issues = []
    ids = Counter(r["student_id"] for r in rows)
    emails = Counter(r["email"].lower() for r in rows)
    for r in rows:
        if ids[r["student_id"]] > 1:
            issues.append(f"{r['student_id']}: duplicate student id")
        if emails[r["email"].lower()] > 1:
            issues.append(f"{r['student_id']}: duplicate email")
        if "@" not in r["email"]:
            issues.append(f"{r['student_id']}: malformed email")
        try:
            value = float(r["attendance_percent"])
            if not 0 <= value <= 100:
                issues.append(f"{r['student_id']}: attendance out of range")
        except ValueError:
            issues.append(f"{r['student_id']}: attendance is not a number")
    for issue in sorted(set(issues)):
        print("  ", issue)
    if not issues:
        print(f"  all {len(rows)} record(s) passed")

    records = [to_record(r) for r in rows]

    if args.group_by_grade:
        grouped = defaultdict(list)
        for rec in records:
            grouped[rec["grade"]].append(rec)
        payload = {"generatedFor": "student portal",
                   "cutoff": ATTENDANCE_CUTOFF,
                   "grades": dict(sorted(grouped.items()))}
    else:
        payload = {"generatedFor": "student portal",
                   "cutoff": ATTENDANCE_CUTOFF,
                   "count": len(records),
                   "students": records}

    with open(args.output, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=args.indent, ensure_ascii=False)

    print(f"\n=== wrote {os.path.basename(args.output)} ===")
    print(f"  size : {os.path.getsize(args.output)} bytes")
    print(f"  shape: {'grouped by grade' if args.group_by_grade else 'flat list'}")

    print("\n=== first two JSON records ===")
    print(json.dumps(records[:2], indent=2))

    print("\n=== grade-wise summary ===")
    by_grade = defaultdict(list)
    for rec in records:
        by_grade[rec["grade"]].append(rec)
    print(f"  {'grade':<9}{'students':>9}{'avg attendance':>17}"
          f"{'below cutoff':>14}")
    for grade in sorted(by_grade):
        group = by_grade[grade]
        avg = sum(s["attendancePercent"] for s in group) / len(group)
        short = sum(1 for s in group if not s["attendanceOk"])
        print(f"  {grade:<9}{len(group):>9}{avg:>16.2f}%{short:>14}")

    print(f"\n=== students below the {ATTENDANCE_CUTOFF}% cutoff ===")
    for rec in sorted(records, key=lambda s: s["attendancePercent"]):
        if not rec["attendanceOk"]:
            short = ATTENDANCE_CUTOFF - rec["attendancePercent"]
            print(f"  {rec['name']:<18}{rec['grade']:<9}"
                  f"{rec['attendancePercent']:>6.1f}%  short by {short:.1f} points")

    print("\n=== section split ===")
    for section, count in Counter(r["section"] for r in records).most_common():
        print(f"  section {section}: {count} student(s)")

    print("\n=== round-trip check ===")
    with open(args.output, "r", encoding="utf-8") as fh:
        reloaded = json.load(fh)
    count = (sum(len(v) for v in reloaded["grades"].values())
             if args.group_by_grade else len(reloaded["students"]))
    print(f"  records reloaded : {count}")
    print(f"  matches CSV      : {count == len(rows)}")
    print(f"  attendance typed as float: "
          f"{isinstance(records[0]['attendancePercent'], float)}")
