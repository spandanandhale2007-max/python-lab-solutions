"""
Experiment 8 - Question 3: Sensor Data Logger

Scenario: An IoT device logs temperature readings into sensor_data.txt line by
line. Count how many readings are recorded, extract the first two readings and
save them in initial_readings.txt.

Run: python q3_sensor_data_logger.py
"""

import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
INPUT_FILE = os.path.join(DATA, "sensor_data.txt")
OUTPUT_FILE = os.path.join(DATA, "initial_readings.txt")

SAFE_LOW, SAFE_HIGH = 2.0, 8.0          # vaccine fridge range in Celsius


def ensure_sample(readings=36):
    """Simulates a vaccine refrigerator logging every 10 minutes."""
    os.makedirs(DATA, exist_ok=True)
    if os.path.exists(INPUT_FILE):
        return
    random.seed(44)
    with open(INPUT_FILE, "w", encoding="utf-8") as fh:
        for i in range(readings):
            hour, minute = divmod(i * 10, 60)
            temp = round(random.uniform(2.5, 7.5), 2)
            if i in (14, 15, 16):                   # door left open
                temp = round(random.uniform(9.0, 12.5), 2)
            if i == 29:
                fh.write("SENSOR_ERROR,--,--\n")    # a bad line
                continue
            fh.write(f"{hour:02d}:{minute:02d},{temp},C\n")
    print(f"[setup] created sample input {INPUT_FILE}")


if __name__ == "__main__":
    ensure_sample()

    with open(INPUT_FILE, "r", encoding="utf-8") as fh:
        raw_lines = [ln.strip() for ln in fh if ln.strip()]

    print(f"=== read {os.path.basename(INPUT_FILE)} ===")
    print(f"  lines recorded : {len(raw_lines)}")
    print(f"  file size      : {os.path.getsize(INPUT_FILE)} bytes")

    readings, bad_lines = [], []
    for line in raw_lines:
        parts = line.split(",")
        try:
            readings.append((parts[0], float(parts[1])))
        except (IndexError, ValueError):
            bad_lines.append(line)

    print(f"  valid readings : {len(readings)}")
    print(f"  bad lines      : {len(bad_lines)} -> {bad_lines}")

    first_two = raw_lines[:2]
    print("\n=== first two readings ===")
    for i, line in enumerate(first_two, 1):
        print(f"  {i}. {line}")

    temps = [t for _, t in readings]
    print("\n=== statistics ===")
    print(f"  minimum : {min(temps):.2f} C at {readings[temps.index(min(temps))][0]}")
    print(f"  maximum : {max(temps):.2f} C at {readings[temps.index(max(temps))][0]}")
    print(f"  average : {sum(temps) / len(temps):.2f} C")
    print(f"  spread  : {max(temps) - min(temps):.2f} C")

    print(f"\n=== safe range check ({SAFE_LOW}-{SAFE_HIGH} C) ===")
    breaches = [(t, v) for t, v in readings if not SAFE_LOW <= v <= SAFE_HIGH]
    if breaches:
        for stamp, value in breaches:
            print(f"  {stamp}  {value:>6.2f} C  OUT OF RANGE "
                  f"({value - SAFE_HIGH:+.2f} C above the ceiling)")
        print(f"\n  {len(breaches)} breach(es) over "
              f"{len(breaches) * 10} minutes - the cold chain was broken")
    else:
        print("  all readings inside the safe range")

    print("\n=== full log with a trace ===")
    for stamp, value in readings:
        flag = "" if SAFE_LOW <= value <= SAFE_HIGH else "  <== ALERT"
        print(f"  {stamp}  {value:>6.2f} C  {'*' * int(value * 2)}{flag}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as fh:
        for line in first_two:
            fh.write(line + "\n")

    print(f"\n=== wrote {OUTPUT_FILE} ===")
    with open(OUTPUT_FILE, "r", encoding="utf-8") as fh:
        for line in fh:
            print("  " + line.rstrip())
    print(f"\n  lines in the output file: "
          f"{sum(1 for _ in open(OUTPUT_FILE, encoding='utf-8'))}")

    print("\n=== device health verdict ===")
    uptime = len(readings) / len(raw_lines) * 100
    print(f"  data completeness : {uptime:.1f}%")
    print(f"  verdict           : " +
          ("sensor healthy, cold chain intact" if not breaches and uptime > 99
           else "cold chain breach logged, review the fridge door"
           if breaches else "sensor dropped readings, check the connection"))
