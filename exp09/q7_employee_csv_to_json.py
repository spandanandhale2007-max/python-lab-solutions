"""
Experiment 9 - Question 7: Employee Directory Export

Scenario: An HR system exports employee details (name, ID, department, email)
to employees.csv. Read that file and convert the data to JSON
(employees.json) for an internal company directory app.

Usage:
  python q7_employee_csv_to_json.py
  python q7_employee_csv_to_json.py --input other.csv --output other.json
"""

import argparse
import csv
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
DEFAULT_CSV = os.path.join(DATA, "employees.csv")
DEFAULT_JSON = os.path.join(DATA, "employees.json")

SAMPLE_CSV = """employee_id,name,department,email,designation,joined
EMP-1001,Spandan Andhale,Engineering,spandan.andhale@company.in,Software Intern,2026-06-01
EMP-1002,Riya Sharma,Design,riya.sharma@company.in,UX Designer,2025-07-14
EMP-1003,Aman Kulkarni,Engineering,aman.kulkarni@company.in,Backend Engineer,2024-01-08
EMP-1004,Neha Deshmukh,Quality,neha.deshmukh@company.in,QA Engineer,2024-09-23
EMP-1005,Omkar Patil,Engineering,omkar.patil@company.in,DevOps Engineer,2023-03-15
EMP-1006,Sana Shaikh,Operations,sana.shaikh@company.in,Operations Lead,2022-11-02
EMP-1007,Kavita Rao,Research,kavita.rao@company.in,Principal Scientist,2021-05-19
EMP-1008,Harsh Mehta,Design,harsh.mehta@company.in,Visual Designer,2025-02-10
"""


def ensure_sample(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8", newline="") as fh:
            fh.write(SAMPLE_CSV)
        print(f"[setup] created sample input {path}")


def read_csv(path):
    with open(path, "r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        rows = [dict(row) for row in reader]
        return rows, reader.fieldnames


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert an employee CSV export into JSON.")
    parser.add_argument("--input", default=DEFAULT_CSV)
    parser.add_argument("--output", default=DEFAULT_JSON)
    parser.add_argument("--indent", type=int, default=2)
    parser.add_argument("--group-by-department", action="store_true")
    args = parser.parse_args()

    ensure_sample(args.input)
    rows, headers = read_csv(args.input)

    print(f"=== read {os.path.basename(args.input)} ===")
    print(f"  columns : {headers}")
    print(f"  records : {len(rows)}")
    print(f"  size    : {os.path.getsize(args.input)} bytes")

    print("\n=== CSV as a table ===")
    widths = {h: max(len(h), max((len(r[h]) for r in rows), default=0))
              for h in headers}
    print("  " + "  ".join(f"{h:<{widths[h]}}" for h in headers))
    print("  " + "-" * (sum(widths.values()) + 2 * len(headers)))
    for r in rows:
        print("  " + "  ".join(f"{r[h]:<{widths[h]}}" for h in headers))

    # --- validation before export ---
    print("\n=== validation ===")
    problems = []
    seen_ids, seen_emails = set(), set()
    for n, r in enumerate(rows, 2):           # line 2 is the first data row
        if not r.get("email") or "@" not in r["email"]:
            problems.append((n, r.get("employee_id"), "invalid email"))
        if r["employee_id"] in seen_ids:
            problems.append((n, r["employee_id"], "duplicate employee id"))
        if r["email"].lower() in seen_emails:
            problems.append((n, r["employee_id"], "duplicate email"))
        seen_ids.add(r["employee_id"])
        seen_emails.add(r["email"].lower())
    if problems:
        for line, emp, why in problems:
            print(f"  line {line}: {emp} -> {why}")
    else:
        print(f"  all {len(rows)} record(s) valid, "
              f"{len(seen_ids)} unique id(s)")

    # --- build the JSON payload the directory app wants ---
    employees = []
    for r in rows:
        employees.append({
            "employeeId": r["employee_id"],
            "name": r["name"],
            "department": r["department"],
            "email": r["email"].lower(),
            "designation": r.get("designation", ""),
            "joined": r.get("joined", ""),
        })

    payload = (employees if not args.group_by_department else
               {"departments": {}})
    if args.group_by_department:
        for e in employees:
            payload["departments"].setdefault(e["department"], []).append(e)

    with open(args.output, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=args.indent, ensure_ascii=False)

    print(f"\n=== wrote {os.path.basename(args.output)} ===")
    print(f"  size   : {os.path.getsize(args.output)} bytes")
    print(f"  records: {len(employees)}")

    print("\n=== first two JSON records ===")
    print(json.dumps(employees[:2], indent=2))

    print("\n=== round-trip check ===")
    with open(args.output, "r", encoding="utf-8") as fh:
        reloaded = json.load(fh)
    count = (len(reloaded) if isinstance(reloaded, list)
             else sum(len(v) for v in reloaded["departments"].values()))
    print(f"  reloaded {count} record(s) from JSON, matches CSV: "
          f"{count == len(rows)}")

    print("\n=== directory summary ===")
    departments = {}
    for e in employees:
        departments.setdefault(e["department"], []).append(e["name"])
    for dept, members in sorted(departments.items()):
        print(f"  {dept:<14}{len(members):>3}  {', '.join(members)}")

    print("\n=== JSON vs CSV size ===")
    csv_size = os.path.getsize(args.input)
    json_size = os.path.getsize(args.output)
    print(f"  CSV  : {csv_size:>6} bytes")
    print(f"  JSON : {json_size:>6} bytes "
          f"({json_size / csv_size:.1f}x larger, the cost of key names)")
    print("  JSON is still the right choice here: the frontend can consume it")
    print("  directly with fetch().then(r => r.json()) and no parsing code.")
