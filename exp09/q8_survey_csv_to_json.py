"""
Experiment 9 - Question 8: Survey Results Dashboard

Scenario: Survey results are stored in survey_results.csv. Convert the data to
JSON (survey_results.json) so a web dashboard can consume it in JavaScript.

Usage:
  python q8_survey_csv_to_json.py
  python q8_survey_csv_to_json.py --input other.csv --output other.json
"""

import argparse
import csv
import json
import os
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
DEFAULT_CSV = os.path.join(DATA, "survey_results.csv")
DEFAULT_JSON = os.path.join(DATA, "survey_results.json")

SAMPLE_CSV = """response_id,timestamp,age_group,city,rating,recommend,comment
R001,2026-11-18 09:14,18-24,Pune,9,yes,Bed availability page saves us phone calls
R002,2026-11-18 10:02,25-34,Mumbai,8,yes,Useful but the data looked stale once
R003,2026-11-18 11:40,35-44,Nashik,10,yes,Exactly what a district hospital needs
R004,2026-11-19 08:21,18-24,Pune,6,no,Mobile layout squeezes the ward names
R005,2026-11-19 09:55,45-54,Nagpur,7,yes,Please add a paediatric bed filter
R006,2026-11-19 12:30,25-34,Mumbai,3,no,Showed a bed as free that was taken
R007,2026-11-20 10:05,35-44,Pune,9,yes,Refresh is fast and colour coding is clear
R008,2026-11-20 14:18,55+,Nashik,10,yes,Front desk answers bed queries without calling
R009,2026-11-21 09:02,25-34,Nagpur,5,no,Fine for one hospital we need a multi view
R010,2026-11-21 16:44,18-24,Pune,8,yes,An SMS alert on low ICU capacity would help
R011,2026-11-22 11:11,45-54,Mumbai,2,no,Could not log in for two days
R012,2026-11-22 13:27,35-44,Pune,9,yes,Clean interface no training needed
"""


def ensure_sample(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8", newline="") as fh:
            fh.write(SAMPLE_CSV)
        print(f"[setup] created sample input {path}")


def typed(row):
    """CSV gives everything as strings; the dashboard wants real types."""
    return {
        "responseId": row["response_id"],
        "timestamp": row["timestamp"],
        "ageGroup": row["age_group"],
        "city": row["city"],
        "rating": int(row["rating"]),
        "recommend": row["recommend"].strip().lower() == "yes",
        "comment": row["comment"],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert survey CSV results into dashboard-ready JSON.")
    parser.add_argument("--input", default=DEFAULT_CSV)
    parser.add_argument("--output", default=DEFAULT_JSON)
    parser.add_argument("--indent", type=int, default=2)
    args = parser.parse_args()

    ensure_sample(args.input)

    with open(args.input, "r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        raw_rows = list(reader)
        headers = reader.fieldnames

    print(f"=== read {os.path.basename(args.input)} ===")
    print(f"  columns   : {headers}")
    print(f"  responses : {len(raw_rows)}")
    print(f"  size      : {os.path.getsize(args.input)} bytes")

    responses = [typed(r) for r in raw_rows]

    print("\n=== type conversion ===")
    sample = raw_rows[0]
    print(f"  CSV  : rating={sample['rating']!r} "
          f"recommend={sample['recommend']!r}  (both strings)")
    print(f"  JSON : rating={responses[0]['rating']!r} "
          f"recommend={responses[0]['recommend']!r}  (int and bool)")

    ratings = [r["rating"] for r in responses]
    promoters = sum(1 for r in ratings if r >= 9)
    detractors = sum(1 for r in ratings if r <= 6)
    nps = (promoters - detractors) / len(ratings) * 100

    by_city = Counter(r["city"] for r in responses)
    by_age = Counter(r["ageGroup"] for r in responses)

    # the aggregates the dashboard needs, computed once here
    summary = {
        "totalResponses": len(responses),
        "averageRating": round(sum(ratings) / len(ratings), 2),
        "minRating": min(ratings),
        "maxRating": max(ratings),
        "recommendCount": sum(1 for r in responses if r["recommend"]),
        "recommendPercent": round(
            sum(1 for r in responses if r["recommend"]) / len(responses) * 100, 1),
        "nps": round(nps, 1),
        "ratingDistribution": {str(k): v for k, v in
                               sorted(Counter(ratings).items())},
        "byCity": dict(by_city),
        "byAgeGroup": dict(sorted(by_age.items())),
    }

    payload = {"summary": summary, "responses": responses}

    with open(args.output, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=args.indent, ensure_ascii=False)

    print(f"\n=== wrote {os.path.basename(args.output)} ===")
    print(f"  size : {os.path.getsize(args.output)} bytes")
    print(f"  shape: {{ summary: {{...}}, responses: [{len(responses)}] }}")

    print("\n=== summary block (what the dashboard tiles read) ===")
    print(json.dumps(summary, indent=2))

    print("\n=== first two response objects ===")
    print(json.dumps(responses[:2], indent=2))

    print("\n=== rating distribution ===")
    for rating, count in sorted(Counter(ratings).items()):
        print(f"  {rating:>2} : {'#' * count} ({count})")

    print("\n=== by city ===")
    for city, count in by_city.most_common():
        city_ratings = [r["rating"] for r in responses if r["city"] == city]
        print(f"  {city:<10}{count:>3} response(s)  "
              f"avg {sum(city_ratings) / len(city_ratings):>5.2f}")

    print("\n=== by age group ===")
    for group, count in sorted(by_age.items()):
        group_ratings = [r["rating"] for r in responses
                         if r["ageGroup"] == group]
        print(f"  {group:<8}{count:>3} response(s)  "
              f"avg {sum(group_ratings) / len(group_ratings):>5.2f}")

    print("\n=== round-trip check ===")
    with open(args.output, "r", encoding="utf-8") as fh:
        reloaded = json.load(fh)
    print(f"  responses reloaded : {len(reloaded['responses'])}")
    print(f"  matches CSV rows   : "
          f"{len(reloaded['responses']) == len(raw_rows)}")
    print(f"  rating is a number : "
          f"{isinstance(reloaded['responses'][0]['rating'], int)}")

    print("\n=== how the frontend consumes it ===")
    print("  fetch('survey_results.json')")
    print("    .then(r => r.json())")
    print("    .then(d => renderTiles(d.summary, d.responses));")
