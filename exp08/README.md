# Experiment 8 - Unit III

File handling: reading files, counting lines, writing summaries

10 scenario questions, each solved in its own section and its own file. Every program below was executed and the real output is included.

[Back to the index](../README.md)

---

## Questions in this experiment

- [Experiment 8 - Question 1: Log File Analysis](#experiment-8---question-1-log-file-analysis)
- [Experiment 8 - Question 2: Student Feedback Collection](#experiment-8---question-2-student-feedback-collection)
- [Experiment 8 - Question 3: Sensor Data Logger](#experiment-8---question-3-sensor-data-logger)
- [Experiment 8 - Question 4: Chat Transcript Preview](#experiment-8---question-4-chat-transcript-preview)
- [Experiment 8 - Question 5: Research Notes Organizer](#experiment-8---question-5-research-notes-organizer)
- [Experiment 8 - Question 6: News Feed Processor](#experiment-8---question-6-news-feed-processor)
- [Experiment 8 - Question 7: Code Snippet Extractor](#experiment-8---question-7-code-snippet-extractor)
- [Experiment 8 - Question 8: Email Archive Preview](#experiment-8---question-8-email-archive-preview)
- [Experiment 8 - Question 9: Survey Responses Handler](#experiment-8---question-9-survey-responses-handler)
- [Experiment 8 - Question 10: Book Chapter Processor](#experiment-8---question-10-book-chapter-processor)

---

## Experiment 8 - Question 1: Log File Analysis

Scenario: A server generates a daily log file (server_log.txt). Read the log,
count the number of log entries (lines), extract the first two log messages
and write them into log_summary.txt for the system administrator.

Run: python q1_log_file_analysis.py

**File:** [`q1_log_file_analysis.py`](q1_log_file_analysis.py) &nbsp;&middot;&nbsp; **Run:** `python q1_log_file_analysis.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
"""
Experiment 8 - Question 1: Log File Analysis

Scenario: A server generates a daily log file (server_log.txt). Read the log,
count the number of log entries (lines), extract the first two log messages
and write them into log_summary.txt for the system administrator.

Run: python q1_log_file_analysis.py
"""

import os
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
INPUT_FILE = os.path.join(DATA, "server_log.txt")
OUTPUT_FILE = os.path.join(DATA, "log_summary.txt")

SAMPLE = """2026-11-24 00:00:12 INFO  nginx started, listening on :443
2026-11-24 00:04:51 INFO  GET /api/beds 200 in 42ms
2026-11-24 00:17:03 WARN  slow query on appointments table, 1840ms
2026-11-24 01:02:44 INFO  GET /api/doctors 200 in 28ms
2026-11-24 01:33:19 ERROR failed to reach supabase: connection reset
2026-11-24 01:33:25 INFO  retry succeeded after 1 attempt
2026-11-24 02:15:08 INFO  nightly backup started
2026-11-24 02:41:55 INFO  nightly backup finished, 184 MB
2026-11-24 06:00:01 INFO  cron: appointment reminders dispatched
2026-11-24 09:12:37 ERROR 500 on POST /api/appointments, payload too large
2026-11-24 09:12:40 WARN  rate limit hit for 49.36.x.x
2026-11-24 14:48:22 INFO  GET /api/medications 200 in 31ms
"""


def ensure_sample():
    os.makedirs(DATA, exist_ok=True)
    if not os.path.exists(INPUT_FILE):
        with open(INPUT_FILE, "w", encoding="utf-8") as fh:
            fh.write(SAMPLE)
        print(f"[setup] created sample input {INPUT_FILE}")


if __name__ == "__main__":
    ensure_sample()

    # --- read the whole log, one line per entry ---
    with open(INPUT_FILE, "r", encoding="utf-8") as fh:
        lines = fh.readlines()

    entries = [ln.rstrip("\n") for ln in lines if ln.strip()]

    print(f"=== read {os.path.basename(INPUT_FILE)} ===")
    print(f"  total lines in the file : {len(lines)}")
    print(f"  non-empty log entries   : {len(entries)}")
    print(f"  file size               : {os.path.getsize(INPUT_FILE)} bytes")

    first_two = entries[:2]
    print("\n=== first two log messages ===")
    for i, entry in enumerate(first_two, 1):
        print(f"  {i}. {entry}")

    print("\n=== last entry, for context ===")
    print(f"  {entries[-1]}")

    # --- severity breakdown, useful for the admin ---
    levels = Counter()
    for entry in entries:
        parts = entry.split()
        if len(parts) >= 3:
            levels[parts[2]] += 1

    print("\n=== severity breakdown ===")
    for level, count in levels.most_common():
        print(f"  {level:<7}{count:>3}  ({count / len(entries) * 100:.1f}%)")

    errors = [e for e in entries if " ERROR " in e]
    warnings = [e for e in entries if " WARN " in e]

    print(f"\n=== {len(errors)} error(s) needing attention ===")
    for e in errors:
        print("  ", e)
    print(f"\n=== {len(warnings)} warning(s) ===")
    for w in warnings:
        print("  ", w)

    # --- write the summary file ---
    with open(OUTPUT_FILE, "w", encoding="utf-8") as fh:
        fh.write(first_two[0] + "\n")
        fh.write(first_two[1] + "\n")

    print(f"\n=== wrote {OUTPUT_FILE} ===")
    with open(OUTPUT_FILE, "r", encoding="utf-8") as fh:
        for line in fh:
            print("  " + line.rstrip())

    print(f"\n  summary file line count: "
          f"{sum(1 for _ in open(OUTPUT_FILE, encoding='utf-8'))}")

    print("\n=== admin one-line verdict ===")
    print(f"  {len(entries)} entries, {levels.get('ERROR', 0)} error(s), "
          f"{levels.get('WARN', 0)} warning(s) - " +
          ("investigate the errors" if errors else "log looks healthy"))
```

</details>

<details>
<summary>Program output</summary>

```text
=== read server_log.txt ===
  total lines in the file : 12
  non-empty log entries   : 12
  file size               : 733 bytes

=== first two log messages ===
  1. 2026-11-24 00:00:12 INFO  nginx started, listening on :443
  2. 2026-11-24 00:04:51 INFO  GET /api/beds 200 in 42ms

=== last entry, for context ===
  2026-11-24 14:48:22 INFO  GET /api/medications 200 in 31ms

=== severity breakdown ===
  INFO     8  (66.7%)
  WARN     2  (16.7%)
  ERROR    2  (16.7%)

=== 2 error(s) needing attention ===
   2026-11-24 01:33:19 ERROR failed to reach supabase: connection reset
   2026-11-24 09:12:37 ERROR 500 on POST /api/appointments, payload too large

=== 2 warning(s) ===
   2026-11-24 00:17:03 WARN  slow query on appointments table, 1840ms
   2026-11-24 09:12:40 WARN  rate limit hit for 49.36.x.x

=== wrote d:\Claude- Hospitalisation Services\python-lab-solutions\exp08\data\log_summary.txt ===
  2026-11-24 00:00:12 INFO  nginx started, listening on :443
  2026-11-24 00:04:51 INFO  GET /api/beds 200 in 42ms

  summary file line count: 2

=== admin one-line verdict ===
  12 entries, 2 error(s), 2 warning(s) - investigate the errors

```

</details>

---

## Experiment 8 - Question 2: Student Feedback Collection

Scenario: Feedback from students arrives in feedback.txt. Read the file, count
the total number of feedback entries and extract the first two responses. Save
the extracted feedback in sample_feedback.txt.

Run: python q2_student_feedback.py

**File:** [`q2_student_feedback.py`](q2_student_feedback.py) &nbsp;&middot;&nbsp; **Run:** `python q2_student_feedback.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
"""
Experiment 8 - Question 2: Student Feedback Collection

Scenario: Feedback from students arrives in feedback.txt. Read the file, count
the total number of feedback entries and extract the first two responses. Save
the extracted feedback in sample_feedback.txt.

Run: python q2_student_feedback.py
"""

import os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
INPUT_FILE = os.path.join(DATA, "feedback.txt")
OUTPUT_FILE = os.path.join(DATA, "sample_feedback.txt")

POSITIVE = ["good", "great", "excellent", "helpful", "clear", "loved",
            "useful", "enjoyed", "best"]
NEGATIVE = ["slow", "boring", "confusing", "difficult", "poor", "rushed",
            "unclear", "too fast"]

SAMPLE = """The Python lab sessions were excellent, the examples were very clear.
Lectures move too fast for a first-year subject, please slow down.
Loved the hospital management case study, it made OOP concepts click.
The assignment deadlines overlap with other subjects, that is difficult.
Good use of real datasets in the pandas unit, very useful.
The projector in Lab 4 keeps failing, it wastes the first ten minutes.
More practice questions on dynamic programming would be helpful.
Teaching is great but the textbook is confusing in places.
The viva format is fair and the feedback afterwards is clear.
Please upload the slides before class, not after.
"""


def ensure_sample():
    os.makedirs(DATA, exist_ok=True)
    if not os.path.exists(INPUT_FILE):
        with open(INPUT_FILE, "w", encoding="utf-8") as fh:
            fh.write(SAMPLE)
        print(f"[setup] created sample input {INPUT_FILE}")


def sentiment(text):
    low = text.lower()
    pos = sum(1 for w in POSITIVE if w in low)
    neg = sum(1 for w in NEGATIVE if w in low)
    if pos > neg:
        return "positive"
    if neg > pos:
        return "negative"
    return "neutral"


if __name__ == "__main__":
    ensure_sample()

    with open(INPUT_FILE, "r", encoding="utf-8") as fh:
        responses = [ln.strip() for ln in fh if ln.strip()]

    print(f"=== read {os.path.basename(INPUT_FILE)} ===")
    print(f"  total feedback entries : {len(responses)}")
    print(f"  file size              : {os.path.getsize(INPUT_FILE)} bytes")
    words = sum(len(r.split()) for r in responses)
    print(f"  total words            : {words}")
    print(f"  average response length: {words / len(responses):.1f} words")

    first_two = responses[:2]
    print("\n=== first two responses ===")
    for i, r in enumerate(first_two, 1):
        print(f"  {i}. {r}")

    print("\n=== all responses with a sentiment tag ===")
    for i, r in enumerate(responses, 1):
        print(f"  {i:>2}. [{sentiment(r):<8}] {r}")

    counts = {}
    for r in responses:
        tag = sentiment(r)
        counts[tag] = counts.get(tag, 0) + 1

    print("\n=== sentiment summary ===")
    for tag in ("positive", "neutral", "negative"):
        n = counts.get(tag, 0)
        bar = "#" * n
        print(f"  {tag:<9}{n:>3}  |{bar}")
    print(f"  satisfaction: "
          f"{counts.get('positive', 0) / len(responses) * 100:.1f}% positive")

    print("\n=== longest and shortest response ===")
    print(f"  longest  ({len(max(responses, key=len))} chars): "
          f"{max(responses, key=len)}")
    print(f"  shortest ({len(min(responses, key=len))} chars): "
          f"{min(responses, key=len)}")

    print("\n=== action items (negative feedback) ===")
    actions = [r for r in responses if sentiment(r) == "negative"]
    for i, r in enumerate(actions, 1):
        print(f"  {i}. {r}")
    if not actions:
        print("  none")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as fh:
        for r in first_two:
            fh.write(r + "\n")

    print(f"\n=== wrote {OUTPUT_FILE} ===")
    with open(OUTPUT_FILE, "r", encoding="utf-8") as fh:
        content = fh.read()
    print(content.rstrip().replace("\n", "\n  ").rjust(0))
    print(f"\n  lines written : {len(content.splitlines())}")
    print(f"  bytes written : {len(content.encode())}")
```

</details>

<details>
<summary>Program output</summary>

```text
=== read feedback.txt ===
  total feedback entries : 10
  file size              : 656 bytes
  total words            : 105
  average response length: 10.5 words

=== first two responses ===
  1. The Python lab sessions were excellent, the examples were very clear.
  2. Lectures move too fast for a first-year subject, please slow down.

=== all responses with a sentiment tag ===
   1. [positive] The Python lab sessions were excellent, the examples were very clear.
   2. [negative] Lectures move too fast for a first-year subject, please slow down.
   3. [positive] Loved the hospital management case study, it made OOP concepts click.
   4. [negative] The assignment deadlines overlap with other subjects, that is difficult.
   5. [positive] Good use of real datasets in the pandas unit, very useful.
   6. [neutral ] The projector in Lab 4 keeps failing, it wastes the first ten minutes.
   7. [positive] More practice questions on dynamic programming would be helpful.
   8. [neutral ] Teaching is great but the textbook is confusing in places.
   9. [positive] The viva format is fair and the feedback afterwards is clear.
  10. [neutral ] Please upload the slides before class, not after.

=== sentiment summary ===
  positive   5  |#####
  neutral    3  |###
  negative   2  |##
  satisfaction: 50.0% positive

=== longest and shortest response ===
  longest  (72 chars): The assignment deadlines overlap with other subjects, that is difficult.
  shortest (49 chars): Please upload the slides before class, not after.

=== action items (negative feedback) ===
  1. Lectures move too fast for a first-year subject, please slow down.
  2. The assignment deadlines overlap with other subjects, that is difficult.

=== wrote d:\Claude- Hospitalisation Services\python-lab-solutions\exp08\data\sample_feedback.txt ===
The Python lab sessions were excellent, the examples were very clear.
  Lectures move too fast for a first-year subject, please slow down.

  lines written : 2
  bytes written : 137

```

</details>

---

## Experiment 8 - Question 3: Sensor Data Logger

Scenario: An IoT device logs temperature readings into sensor_data.txt line by
line. Count how many readings are recorded, extract the first two readings and
save them in initial_readings.txt.

Run: python q3_sensor_data_logger.py

**File:** [`q3_sensor_data_logger.py`](q3_sensor_data_logger.py) &nbsp;&middot;&nbsp; **Run:** `python q3_sensor_data_logger.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
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
```

</details>

<details>
<summary>Program output</summary>

```text
=== read sensor_data.txt ===
  lines recorded : 36
  file size      : 512 bytes
  valid readings : 35
  bad lines      : 1 -> ['SENSOR_ERROR,--,--']

=== first two readings ===
  1. 00:00,4.54,C
  2. 00:10,5.21,C

=== statistics ===
  minimum : 2.54 C at 01:10
  maximum : 11.95 C at 02:30
  average : 5.09 C
  spread  : 9.41 C

=== safe range check (2.0-8.0 C) ===
  02:20   10.14 C  OUT OF RANGE (+2.14 C above the ceiling)
  02:30   11.95 C  OUT OF RANGE (+3.95 C above the ceiling)
  02:40    9.39 C  OUT OF RANGE (+1.39 C above the ceiling)

  3 breach(es) over 30 minutes - the cold chain was broken

=== full log with a trace ===
  00:00    4.54 C  *********
  00:10    5.21 C  **********
  00:20    6.81 C  *************
  00:30    3.38 C  ******
  00:40    3.63 C  *******
  00:50    2.65 C  *****
  01:00    3.08 C  ******
  01:10    2.54 C  *****
  01:20    3.28 C  ******
  01:30    5.07 C  **********
  01:40    7.45 C  **************
  01:50    5.97 C  ***********
  02:00    4.39 C  ********
  02:10    4.53 C  *********
  02:20   10.14 C  ********************  <== ALERT
  02:30   11.95 C  ***********************  <== ALERT
  02:40    9.39 C  ******************  <== ALERT
  02:50    2.85 C  *****
  03:00    2.97 C  *****
  03:10    7.29 C  **************
  03:20    3.04 C  ******
  03:30    5.63 C  ***********
  03:40    7.35 C  **************
  03:50    2.68 C  *****
  04:00    4.43 C  ********
  04:10    4.89 C  *********
  04:20    7.08 C  **************
  04:30    3.44 C  ******
  04:40    3.79 C  *******
  05:00    2.75 C  *****
  05:10    5.87 C  ***********
  05:20    6.58 C  *************
  05:30    4.68 C  *********
  05:40    2.69 C  *****
  05:50    6.07 C  ************

=== wrote d:\Claude- Hospitalisation Services\python-lab-solutions\exp08\data\initial_readings.txt ===
  00:00,4.54,C
  00:10,5.21,C

  lines in the output file: 2

=== device health verdict ===
  data completeness : 97.2%
  verdict           : cold chain breach logged, review the fridge door

```

</details>

---

## Experiment 8 - Question 4: Chat Transcript Preview

Scenario: A chat application stores chat history in chat_history.txt. Generate
a preview containing the number of messages and the first two messages, then
write the preview to chat_preview.txt.

Run: python q4_chat_transcript_preview.py

**File:** [`q4_chat_transcript_preview.py`](q4_chat_transcript_preview.py) &nbsp;&middot;&nbsp; **Run:** `python q4_chat_transcript_preview.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
"""
Experiment 8 - Question 4: Chat Transcript Preview

Scenario: A chat application stores chat history in chat_history.txt. Generate
a preview containing the number of messages and the first two messages, then
write the preview to chat_preview.txt.

Run: python q4_chat_transcript_preview.py
"""

import os
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
INPUT_FILE = os.path.join(DATA, "chat_history.txt")
OUTPUT_FILE = os.path.join(DATA, "chat_preview.txt")

SAMPLE = """[09:02] Spandan: good morning, is the bed availability API live?
[09:03] Riya: yes, deployed last night on Netlify
[09:03] Spandan: great, I will wire the ward panel to it today
[09:05] Aman: careful, the ward panel state is browser-local right now
[09:06] Spandan: right, cross-user sync is still pending
[09:11] Riya: shall I add a loading skeleton to the doctor list?
[09:12] Spandan: yes please, it flashes empty on slow networks
[09:20] Aman: pushed a fix for the appointment duplicate bug
[09:21] Spandan: thanks, I will pull and test
[09:35] Riya: screenshots for the deck are in the shared drive
[09:36] Spandan: perfect, the coordinator wants real screenshots not mockups
[09:40] Aman: standup at 10?
[09:41] Riya: works for me
[09:41] Spandan: see you then
"""


def ensure_sample():
    os.makedirs(DATA, exist_ok=True)
    if not os.path.exists(INPUT_FILE):
        with open(INPUT_FILE, "w", encoding="utf-8") as fh:
            fh.write(SAMPLE)
        print(f"[setup] created sample input {INPUT_FILE}")


def parse(line):
    """[09:02] Spandan: text -> (time, sender, text)"""
    try:
        stamp, rest = line.split("] ", 1)
        sender, text = rest.split(": ", 1)
        return stamp.lstrip("["), sender, text
    except ValueError:
        return None, None, line


if __name__ == "__main__":
    ensure_sample()

    with open(INPUT_FILE, "r", encoding="utf-8") as fh:
        messages = [ln.rstrip("\n") for ln in fh if ln.strip()]

    print(f"=== read {os.path.basename(INPUT_FILE)} ===")
    print(f"  message count : {len(messages)}")
    print(f"  file size     : {os.path.getsize(INPUT_FILE)} bytes")

    parsed = [parse(m) for m in messages]
    senders = Counter(s for _, s, _ in parsed if s)
    print(f"  participants  : {len(senders)}")

    first_two = messages[:2]
    print("\n=== first two messages ===")
    for i, m in enumerate(first_two, 1):
        print(f"  {i}. {m}")

    print("\n=== participation ===")
    for sender, count in senders.most_common():
        share = count / len(messages) * 100
        print(f"  {sender:<10}{count:>3} message(s)  {share:>5.1f}%  "
              f"{'#' * count}")

    words = Counter()
    for _, _, text in parsed:
        words.update(w.strip(".,?!").lower() for w in text.split()
                     if len(w) > 4)
    print("\n=== most used words (5+ letters) ===")
    for word, count in words.most_common(6):
        print(f"  {word:<16}{count}")

    first_time = parsed[0][0]
    last_time = parsed[-1][0]
    print(f"\n=== timeline ===")
    print(f"  first message : {first_time}")
    print(f"  last message  : {last_time}")

    def minutes(stamp):
        h, m = stamp.split(":")
        return int(h) * 60 + int(m)

    span = minutes(last_time) - minutes(first_time)
    print(f"  conversation span : {span} minutes")
    print(f"  message rate      : {len(messages) / max(span, 1) * 60:.1f} "
          f"messages/hour")

    longest = max(parsed, key=lambda p: len(p[2]))
    print(f"\n  longest message: [{longest[0]}] {longest[1]}: "
          f"{longest[2][:50]}... ({len(longest[2])} chars)")

    # --- write the preview file ---
    with open(OUTPUT_FILE, "w", encoding="utf-8") as fh:
        fh.write(f"Total messages: {len(messages)}\n")
        fh.write(first_two[0] + "\n")
        fh.write(first_two[1] + "\n")

    print(f"\n=== wrote {OUTPUT_FILE} ===")
    with open(OUTPUT_FILE, "r", encoding="utf-8") as fh:
        for line in fh:
            print("  " + line.rstrip())

    print(f"\n  preview file: "
          f"{sum(1 for _ in open(OUTPUT_FILE, encoding='utf-8'))} line(s), "
          f"{os.path.getsize(OUTPUT_FILE)} bytes")
    print(f"  compression  : the preview is "
          f"{os.path.getsize(OUTPUT_FILE) / os.path.getsize(INPUT_FILE) * 100:.1f}% "
          f"of the original transcript")
```

</details>

<details>
<summary>Program output</summary>

```text
=== read chat_history.txt ===
  message count : 14
  file size     : 781 bytes
  participants  : 3

=== first two messages ===
  1. [09:02] Spandan: good morning, is the bed availability API live?
  2. [09:03] Riya: yes, deployed last night on Netlify

=== participation ===
  Spandan     7 message(s)   50.0%  #######
  Riya        4 message(s)   28.6%  ####
  Aman        3 message(s)   21.4%  ###

=== most used words (5+ letters) ===
  panel           2
  right           2
  screenshots     2
  morning         1
  availability    1
  live            1

=== timeline ===
  first message : 09:02
  last message  : 09:41
  conversation span : 39 minutes
  message rate      : 21.5 messages/hour

  longest message: [09:36] Spandan: perfect, the coordinator wants real screenshots no... (59 chars)

=== wrote d:\Claude- Hospitalisation Services\python-lab-solutions\exp08\data\chat_preview.txt ===
  Total messages: 14
  [09:02] Spandan: good morning, is the bed availability API live?
  [09:03] Riya: yes, deployed last night on Netlify

  preview file: 3 line(s), 137 bytes
  compression  : the preview is 17.5% of the original transcript

```

</details>

---

## Experiment 8 - Question 5: Research Notes Organizer

Scenario: A research assistant adds daily notes to research_notes.txt.
Summarise the total number of notes, extract the first two entries and save
them into note_summary.txt.

Run: python q5_research_notes_organizer.py

**File:** [`q5_research_notes_organizer.py`](q5_research_notes_organizer.py) &nbsp;&middot;&nbsp; **Run:** `python q5_research_notes_organizer.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
"""
Experiment 8 - Question 5: Research Notes Organizer

Scenario: A research assistant adds daily notes to research_notes.txt.
Summarise the total number of notes, extract the first two entries and save
them into note_summary.txt.

Run: python q5_research_notes_organizer.py
"""

import os
import re
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
INPUT_FILE = os.path.join(DATA, "research_notes.txt")
OUTPUT_FILE = os.path.join(DATA, "note_summary.txt")

DATE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})")
TAG_RE = re.compile(r"#(\w+)")

SAMPLE = """2026-11-10 #literature Read Kumar et al. on hospital bed allocation; queueing model, not ML.
2026-11-11 #dataset Found the open AIIMS bed occupancy dataset, 14 months, hourly granularity.
2026-11-12 #method Tried a simple moving average baseline; MAE 4.2 beds, surprisingly hard to beat.
2026-11-13 #literature Chen 2024 argues occupancy is seasonal at the week level, matches our data.
2026-11-14 #method Added day-of-week features; MAE drops to 3.1 beds.
2026-11-17 #dataset Cleaned 312 duplicate rows caused by the double-logging bug.
2026-11-18 #meeting Coordinator wants a demo with real screenshots by 30 November.
2026-11-19 #method Tried gradient boosting; MAE 2.6 but the model is hard to explain in a viva.
2026-11-20 #writing Drafted the methodology section, 900 words.
2026-11-21 #todo Need an ablation table and one clear figure of weekly seasonality.
2026-11-24 #writing Rewrote the introduction after feedback; tightened the problem statement.
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
        notes = [ln.rstrip("\n") for ln in fh if ln.strip()]

    print(f"=== read {os.path.basename(INPUT_FILE)} ===")
    print(f"  total notes : {len(notes)}")
    print(f"  file size   : {os.path.getsize(INPUT_FILE)} bytes")
    words = sum(len(n.split()) for n in notes)
    print(f"  total words : {words}")
    print(f"  average note: {words / len(notes):.1f} words")

    first_two = notes[:2]
    print("\n=== first two entries ===")
    for i, n in enumerate(first_two, 1):
        print(f"  {i}. {n}")

    dates = [DATE_RE.match(n).group(1) for n in notes if DATE_RE.match(n)]
    print("\n=== date coverage ===")
    print(f"  first entry : {dates[0]}")
    print(f"  last entry  : {dates[-1]}")
    print(f"  distinct days with notes : {len(set(dates))}")
    busiest = Counter(dates).most_common(1)[0]
    print(f"  busiest day : {busiest[0]} with {busiest[1]} note(s)")

    tags = Counter()
    for n in notes:
        tags.update(TAG_RE.findall(n))
    print("\n=== notes by tag ===")
    for tag, count in tags.most_common():
        print(f"  #{tag:<14}{count:>3}  {'#' * count}")

    print("\n=== notes grouped by tag ===")
    for tag, _ in tags.most_common():
        print(f"\n  #{tag}")
        for n in notes:
            if tag in TAG_RE.findall(n):
                print(f"    {n[:78]}")

    todos = [n for n in notes if "#todo" in n]
    print(f"\n=== open action items ({len(todos)}) ===")
    for t in todos:
        print("  ", t)
    if not todos:
        print("  none")

    print("\n=== progress on the stated metric ===")
    for n in notes:
        m = re.search(r"MAE ([\d.]+)", n)
        if m:
            print(f"  {DATE_RE.match(n).group(1)}  MAE {m.group(1)} beds")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as fh:
        fh.write(f"Total notes: {len(notes)}\n")
        fh.write(f"Period: {dates[0]} to {dates[-1]}\n")
        fh.write("First two entries:\n")
        for n in first_two:
            fh.write(n + "\n")

    print(f"\n=== wrote {OUTPUT_FILE} ===")
    with open(OUTPUT_FILE, "r", encoding="utf-8") as fh:
        for line in fh:
            print("  " + line.rstrip())
    print(f"\n  summary file: "
          f"{sum(1 for _ in open(OUTPUT_FILE, encoding='utf-8'))} line(s)")
```

</details>

<details>
<summary>Program output</summary>

```text
=== read research_notes.txt ===
  total notes : 11
  file size   : 970 bytes
  total words : 139
  average note: 12.6 words

=== first two entries ===
  1. 2026-11-10 #literature Read Kumar et al. on hospital bed allocation; queueing model, not ML.
  2. 2026-11-11 #dataset Found the open AIIMS bed occupancy dataset, 14 months, hourly granularity.

=== date coverage ===
  first entry : 2026-11-10
  last entry  : 2026-11-24
  distinct days with notes : 11
  busiest day : 2026-11-10 with 1 note(s)

=== notes by tag ===
  #method          3  ###
  #literature      2  ##
  #dataset         2  ##
  #writing         2  ##
  #meeting         1  #
  #todo            1  #

=== notes grouped by tag ===

  #method
    2026-11-12 #method Tried a simple moving average baseline; MAE 4.2 beds, surpr
    2026-11-14 #method Added day-of-week features; MAE drops to 3.1 beds.
    2026-11-19 #method Tried gradient boosting; MAE 2.6 but the model is hard to e

  #literature
    2026-11-10 #literature Read Kumar et al. on hospital bed allocation; queueing 
    2026-11-13 #literature Chen 2024 argues occupancy is seasonal at the week leve

  #dataset
    2026-11-11 #dataset Found the open AIIMS bed occupancy dataset, 14 months, hou
    2026-11-17 #dataset Cleaned 312 duplicate rows caused by the double-logging bu

  #writing
    2026-11-20 #writing Drafted the methodology section, 900 words.
    2026-11-24 #writing Rewrote the introduction after feedback; tightened the pro

  #meeting
    2026-11-18 #meeting Coordinator wants a demo with real screenshots by 30 Novem

  #todo
    2026-11-21 #todo Need an ablation table and one clear figure of weekly seasona

=== open action items (1) ===
   2026-11-21 #todo Need an ablation table and one clear figure of weekly seasonality.

=== progress on the stated metric ===
  2026-11-12  MAE 4.2 beds
  2026-11-19  MAE 2.6 beds

=== wrote d:\Claude- Hospitalisation Services\python-lab-solutions\exp08\data\note_summary.txt ===
  Total notes: 11
  Period: 2026-11-10 to 2026-11-24
  First two entries:
  2026-11-10 #literature Read Kumar et al. on hospital bed allocation; queueing model, not ML.
  2026-11-11 #dataset Found the open AIIMS bed occupancy dataset, 14 months, hourly granularity.

  summary file: 5 line(s)

```

</details>

---

## Experiment 8 - Question 6: News Feed Processor

Scenario: news_feed.txt contains headlines fetched from a news API. Count how
many headlines were fetched, extract the first two and save them to
top_stories.txt.

Run: python q6_news_feed_processor.py

**File:** [`q6_news_feed_processor.py`](q6_news_feed_processor.py) &nbsp;&middot;&nbsp; **Run:** `python q6_news_feed_processor.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
"""
Experiment 8 - Question 6: News Feed Processor

Scenario: news_feed.txt contains headlines fetched from a news API. Count how
many headlines were fetched, extract the first two and save them to
top_stories.txt.

Run: python q6_news_feed_processor.py
"""

import os
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
INPUT_FILE = os.path.join(DATA, "news_feed.txt")
OUTPUT_FILE = os.path.join(DATA, "top_stories.txt")

SAMPLE = """HEALTH|State expands free dialysis scheme to 40 more district hospitals
TECH|Open-source hospital information system crosses 500 deployments
HEALTH|Monsoon dengue cases drop 18 percent after ward-level surveillance
POLICY|Draft rules would require bed-availability dashboards at every district hospital
TECH|Researchers release an anonymised bed-occupancy dataset covering 14 months
EDUCATION|Engineering syllabus adds a mandatory data-handling lab from next term
HEALTH|Vaccine cold-chain audit flags 12 percent of rural units
TECH|Low-cost IoT temperature logger passes field trial in two districts
POLICY|Health ministry proposes a single appointment booking standard
EDUCATION|Two universities open joint health-informatics programme
HEALTH|Blood bank network goes live across six cities
TECH|Hospital chatbot pilot reduces front-desk queue times by a third
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
        raw = [ln.rstrip("\n") for ln in fh if ln.strip()]

    print(f"=== read {os.path.basename(INPUT_FILE)} ===")
    print(f"  headlines fetched : {len(raw)}")
    print(f"  file size         : {os.path.getsize(INPUT_FILE)} bytes")

    items = []
    for line in raw:
        section, _, headline = line.partition("|")
        items.append((section.strip(), headline.strip() or section.strip()))

    first_two = raw[:2]
    print("\n=== first two headlines ===")
    for i, line in enumerate(first_two, 1):
        section, _, headline = line.partition("|")
        print(f"  {i}. [{section}] {headline}")

    print("\n=== all headlines by section ===")
    sections = Counter(s for s, _ in items)
    for section, count in sections.most_common():
        print(f"\n  {section} ({count})")
        for s, headline in items:
            if s == section:
                print(f"    - {headline}")

    print("\n=== section share ===")
    for section, count in sections.most_common():
        share = count / len(items) * 100
        print(f"  {section:<11}{count:>3}  {share:>5.1f}%  {'#' * count}")

    lengths = [len(h) for _, h in items]
    print("\n=== headline length ===")
    print(f"  shortest : {min(lengths)} chars - "
          f"{min((h for _, h in items), key=len)}")
    print(f"  longest  : {max(lengths)} chars - "
          f"{max((h for _, h in items), key=len)}")
    print(f"  average  : {sum(lengths) / len(lengths):.1f} chars")

    words = Counter()
    stop = {"the", "and", "for", "with", "from", "that", "would", "after",
            "every", "more", "two", "its"}
    for _, h in items:
        words.update(w.strip(".,").lower() for w in h.split()
                     if len(w) > 3 and w.lower() not in stop)
    print("\n=== trending terms ===")
    for word, count in words.most_common(8):
        print(f"  {word:<16}{count}")

    print("\n=== headlines mentioning 'hospital' ===")
    for s, h in items:
        if "hospital" in h.lower():
            print(f"  [{s}] {h}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as fh:
        for line in first_two:
            _, _, headline = line.partition("|")
            fh.write(headline.strip() + "\n")

    print(f"\n=== wrote {OUTPUT_FILE} ===")
    with open(OUTPUT_FILE, "r", encoding="utf-8") as fh:
        for i, line in enumerate(fh, 1):
            print(f"  {i}. {line.rstrip()}")

    print(f"\n  top_stories.txt holds "
          f"{sum(1 for _ in open(OUTPUT_FILE, encoding='utf-8'))} headline(s) "
          f"out of {len(raw)} fetched")
```

</details>

<details>
<summary>Program output</summary>

```text
=== read news_feed.txt ===
  headlines fetched : 12
  file size         : 874 bytes

=== first two headlines ===
  1. [HEALTH] State expands free dialysis scheme to 40 more district hospitals
  2. [TECH] Open-source hospital information system crosses 500 deployments

=== all headlines by section ===

  HEALTH (4)
    - State expands free dialysis scheme to 40 more district hospitals
    - Monsoon dengue cases drop 18 percent after ward-level surveillance
    - Vaccine cold-chain audit flags 12 percent of rural units
    - Blood bank network goes live across six cities

  TECH (4)
    - Open-source hospital information system crosses 500 deployments
    - Researchers release an anonymised bed-occupancy dataset covering 14 months
    - Low-cost IoT temperature logger passes field trial in two districts
    - Hospital chatbot pilot reduces front-desk queue times by a third

  POLICY (2)
    - Draft rules would require bed-availability dashboards at every district hospital
    - Health ministry proposes a single appointment booking standard

  EDUCATION (2)
    - Engineering syllabus adds a mandatory data-handling lab from next term
    - Two universities open joint health-informatics programme

=== section share ===
  HEALTH       4   33.3%  ####
  TECH         4   33.3%  ####
  POLICY       2   16.7%  ##
  EDUCATION    2   16.7%  ##

=== headline length ===
  shortest : 46 chars - Blood bank network goes live across six cities
  longest  : 80 chars - Draft rules would require bed-availability dashboards at every district hospital
  average  : 64.0 chars

=== trending terms ===
  hospital        3
  district        2
  percent         2
  state           1
  expands         1
  free            1
  dialysis        1
  scheme          1

=== headlines mentioning 'hospital' ===
  [HEALTH] State expands free dialysis scheme to 40 more district hospitals
  [TECH] Open-source hospital information system crosses 500 deployments
  [POLICY] Draft rules would require bed-availability dashboards at every district hospital
  [TECH] Hospital chatbot pilot reduces front-desk queue times by a third

=== wrote d:\Claude- Hospitalisation Services\python-lab-solutions\exp08\data\top_stories.txt ===
  1. State expands free dialysis scheme to 40 more district hospitals
  2. Open-source hospital information system crosses 500 deployments

  top_stories.txt holds 2 headline(s) out of 12 fetched

```

</details>

---

## Experiment 8 - Question 7: Code Snippet Extractor

Scenario: snippets.py contains several code snippets. Count how many lines of
code there are and extract the first two lines, writing them to
snippet_preview.py.

Run: python q7_code_snippet_extractor.py

**File:** [`q7_code_snippet_extractor.py`](q7_code_snippet_extractor.py) &nbsp;&middot;&nbsp; **Run:** `python q7_code_snippet_extractor.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
"""
Experiment 8 - Question 7: Code Snippet Extractor

Scenario: snippets.py contains several code snippets. Count how many lines of
code there are and extract the first two lines, writing them to
snippet_preview.py.

Run: python q7_code_snippet_extractor.py
"""

import os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
INPUT_FILE = os.path.join(DATA, "snippets.py")
OUTPUT_FILE = os.path.join(DATA, "snippet_preview.py")

SAMPLE = '''"""Collected snippets from the Python lab."""
import math

# snippet 1: average of a list
def average(values):
    return sum(values) / len(values) if values else 0.0


# snippet 2: Fibonacci generator
def fib():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


# snippet 3: circle area
def circle_area(r):
    return math.pi * r ** 2


# snippet 4: read a file into a list of lines
def read_lines(path):
    with open(path, encoding="utf-8") as fh:
        return [line.rstrip("\\n") for line in fh]


class Counter:
    """snippet 5: a tiny counter class"""

    def __init__(self):
        self.n = 0

    def tick(self):
        self.n += 1
        return self.n
'''


def ensure_sample():
    os.makedirs(DATA, exist_ok=True)
    if not os.path.exists(INPUT_FILE):
        with open(INPUT_FILE, "w", encoding="utf-8") as fh:
            fh.write(SAMPLE)
        print(f"[setup] created sample input {INPUT_FILE}")


def classify(line):
    stripped = line.strip()
    if not stripped:
        return "blank"
    if stripped.startswith("#"):
        return "comment"
    if stripped.startswith(("def ", "async def ")):
        return "function"
    if stripped.startswith("class "):
        return "class"
    if stripped.startswith(("import ", "from ")):
        return "import"
    return "code"


if __name__ == "__main__":
    ensure_sample()

    with open(INPUT_FILE, "r", encoding="utf-8") as fh:
        lines = fh.read().splitlines()

    print(f"=== read {os.path.basename(INPUT_FILE)} ===")
    print(f"  total lines        : {len(lines)}")
    print(f"  file size          : {os.path.getsize(INPUT_FILE)} bytes")

    kinds = {}
    for line in lines:
        k = classify(line)
        kinds[k] = kinds.get(k, 0) + 1

    print("\n=== line breakdown ===")
    for kind in ("import", "class", "function", "code", "comment", "blank"):
        n = kinds.get(kind, 0)
        print(f"  {kind:<10}{n:>4}  {'#' * n}")
    loc = len(lines) - kinds.get("blank", 0) - kinds.get("comment", 0)
    print(f"\n  effective lines of code (no blanks or comments): {loc}")
    print(f"  comment density : "
          f"{kinds.get('comment', 0) / len(lines) * 100:.1f}%")

    first_two = lines[:2]
    print("\n=== first two lines ===")
    for i, line in enumerate(first_two, 1):
        print(f"  {i}. {line!r}")

    print("\n=== functions and classes defined ===")
    for n, line in enumerate(lines, 1):
        kind = classify(line)
        if kind in ("function", "class"):
            name = line.strip().split()[1].split("(")[0].rstrip(":")
            print(f"  line {n:>3}  {kind:<9}{name}")

    print("\n=== imports ===")
    for n, line in enumerate(lines, 1):
        if classify(line) == "import":
            print(f"  line {n:>3}  {line.strip()}")

    print("\n=== longest lines (style check, 79-char limit) ===")
    long_lines = [(n, line) for n, line in enumerate(lines, 1)
                  if len(line) > 79]
    if long_lines:
        for n, line in long_lines:
            print(f"  line {n:>3}  {len(line)} chars")
    else:
        print(f"  none, the longest line is "
              f"{max(len(line) for line in lines)} chars")

    print("\n=== indentation depth ===")
    depths = {}
    for line in lines:
        if line.strip():
            indent = len(line) - len(line.lstrip())
            depths[indent] = depths.get(indent, 0) + 1
    for indent in sorted(depths):
        print(f"  {indent:>2} space(s): {depths[indent]:>3} line(s)")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as fh:
        for line in first_two:
            fh.write(line + "\n")

    print(f"\n=== wrote {OUTPUT_FILE} ===")
    with open(OUTPUT_FILE, "r", encoding="utf-8") as fh:
        for i, line in enumerate(fh, 1):
            print(f"  {i}: {line.rstrip()}")

    print(f"\n  preview holds "
          f"{sum(1 for _ in open(OUTPUT_FILE, encoding='utf-8'))} of "
          f"{len(lines)} lines "
          f"({2 / len(lines) * 100:.1f}% of the file)")
```

</details>

<details>
<summary>Program output</summary>

```text
=== read snippets.py ===
  total lines        : 36
  file size          : 727 bytes

=== line breakdown ===
  import       1  #
  class        1  #
  function     6  ######
  code        13  #############
  comment      4  ####
  blank       11  ###########

  effective lines of code (no blanks or comments): 21
  comment density : 11.1%

=== first two lines ===
  1. '"""Collected snippets from the Python lab."""'
  2. 'import math'

=== functions and classes defined ===
  line   5  function average
  line  10  function fib
  line  18  function circle_area
  line  23  function read_lines
  line  28  class    Counter
  line  31  function __init__
  line  34  function tick

=== imports ===
  line   2  import math

=== longest lines (style check, 79-char limit) ===
  none, the longest line is 55 chars

=== indentation depth ===
   0 space(s):  11 line(s)
   4 space(s):   8 line(s)
   8 space(s):   6 line(s)

=== wrote d:\Claude- Hospitalisation Services\python-lab-solutions\exp08\data\snippet_preview.py ===
  1: """Collected snippets from the Python lab."""
  2: import math

  preview holds 2 of 36 lines (5.6% of the file)

```

</details>

---

## Experiment 8 - Question 8: Email Archive Preview

Scenario: An email application archives raw emails in email_archive.txt. Read
the archive, count how many emails (lines) there are, extract the first two
and save them to email_preview.txt.

Run: python q8_email_archive_preview.py

**File:** [`q8_email_archive_preview.py`](q8_email_archive_preview.py) &nbsp;&middot;&nbsp; **Run:** `python q8_email_archive_preview.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
"""
Experiment 8 - Question 8: Email Archive Preview

Scenario: An email application archives raw emails in email_archive.txt. Read
the archive, count how many emails (lines) there are, extract the first two
and save them to email_preview.txt.

Run: python q8_email_archive_preview.py
"""

import os
import re
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
INPUT_FILE = os.path.join(DATA, "email_archive.txt")
OUTPUT_FILE = os.path.join(DATA, "email_preview.txt")

ROW_RE = re.compile(r"^(?P<date>\d{4}-\d{2}-\d{2})\s+\|\s+"
                    r"(?P<sender>[^|]+)\s+\|\s+(?P<subject>[^|]+)\s+\|\s+"
                    r"(?P<flags>.*)$")

SAMPLE = """2026-11-20 | coordinator@mitwpu.edu.in | Project review slot confirmed | unread,important
2026-11-20 | riya93@mitwpu.edu.in | Re: screenshots for the deck | read
2026-11-21 | noreply@netlify.com | Deploy succeeded for mediverse | read
2026-11-21 | aman_k99@sub.domain.co.in | Pull request #14 ready | unread
2026-11-22 | noreply@github.com | [MediVerse] 2 new issues opened | read
2026-11-22 | support@supabase.io | Your project usage this month | read
2026-11-23 | coordinator@mitwpu.edu.in | Reminder: submit by 30 November | unread,important
2026-11-23 | spam.offers@deals.top | YOU WON a free laptop!! | spam
2026-11-24 | neha.deshmukh@gmail.com | Can you review my pandas notebook | unread
2026-11-24 | noreply@netlify.com | Deploy failed for mediverse | unread,important
2026-11-25 | riya93@mitwpu.edu.in | Final deck draft attached | unread
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
        lines = [ln.rstrip("\n") for ln in fh if ln.strip()]

    print(f"=== read {os.path.basename(INPUT_FILE)} ===")
    print(f"  emails archived (lines) : {len(lines)}")
    print(f"  file size               : {os.path.getsize(INPUT_FILE)} bytes")

    mails = []
    for line in lines:
        m = ROW_RE.match(line)
        if m:
            mails.append({
                "date": m.group("date"),
                "sender": m.group("sender").strip(),
                "subject": m.group("subject").strip(),
                "flags": [f.strip() for f in m.group("flags").split(",")
                          if f.strip()],
            })
    print(f"  parsed successfully     : {len(mails)}")

    first_two = lines[:2]
    print("\n=== first two emails ===")
    for i, line in enumerate(first_two, 1):
        print(f"  {i}. {line}")

    print("\n=== inbox listing ===")
    print(f"  {'date':<12}{'from':<36}{'subject':<38}flags")
    print("  " + "-" * 104)
    for m in mails:
        marker = "*" if "important" in m["flags"] else " "
        print(f"{marker} {m['date']:<12}{m['sender'][:34]:<36}"
              f"{m['subject'][:36]:<38}{','.join(m['flags'])}")

    unread = [m for m in mails if "unread" in m["flags"]]
    important = [m for m in mails if "important" in m["flags"]]
    spam = [m for m in mails if "spam" in m["flags"]]

    print("\n=== counts ===")
    print(f"  total   : {len(mails)}")
    print(f"  unread  : {len(unread)}")
    print(f"  important: {len(important)}")
    print(f"  spam    : {len(spam)}")
    print(f"  read    : {len(mails) - len(unread) - len(spam)}")

    print("\n=== top senders ===")
    senders = Counter(m["sender"] for m in mails)
    for sender, count in senders.most_common():
        print(f"  {sender:<40}{count}")

    print("\n=== domains ===")
    domains = Counter(m["sender"].split("@")[1] for m in mails)
    for d, c in domains.most_common():
        print(f"  {d:<26}{c}")

    print("\n=== needs a reply (unread and important) ===")
    for m in mails:
        if "unread" in m["flags"] and "important" in m["flags"]:
            print(f"  {m['date']}  {m['sender']:<36}{m['subject']}")

    print("\n=== emails per day ===")
    per_day = Counter(m["date"] for m in mails)
    for day in sorted(per_day):
        print(f"  {day}  {per_day[day]}  {'#' * per_day[day]}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as fh:
        fh.write(f"Emails in archive: {len(lines)}\n")
        for line in first_two:
            fh.write(line + "\n")

    print(f"\n=== wrote {OUTPUT_FILE} ===")
    with open(OUTPUT_FILE, "r", encoding="utf-8") as fh:
        for line in fh:
            print("  " + line.rstrip())
    print(f"\n  preview file: "
          f"{sum(1 for _ in open(OUTPUT_FILE, encoding='utf-8'))} line(s), "
          f"{os.path.getsize(OUTPUT_FILE)} bytes")
```

</details>

<details>
<summary>Program output</summary>

```text
=== read email_archive.txt ===
  emails archived (lines) : 11
  file size               : 859 bytes
  parsed successfully     : 11

=== first two emails ===
  1. 2026-11-20 | coordinator@mitwpu.edu.in | Project review slot confirmed | unread,important
  2. 2026-11-20 | riya93@mitwpu.edu.in | Re: screenshots for the deck | read

=== inbox listing ===
  date        from                                subject                               flags
  --------------------------------------------------------------------------------------------------------
* 2026-11-20  coordinator@mitwpu.edu.in           Project review slot confirmed         unread,important
  2026-11-20  riya93@mitwpu.edu.in                Re: screenshots for the deck          read
  2026-11-21  noreply@netlify.com                 Deploy succeeded for mediverse        read
  2026-11-21  aman_k99@sub.domain.co.in           Pull request #14 ready                unread
  2026-11-22  noreply@github.com                  [MediVerse] 2 new issues opened       read
  2026-11-22  support@supabase.io                 Your project usage this month         read
* 2026-11-23  coordinator@mitwpu.edu.in           Reminder: submit by 30 November       unread,important
  2026-11-23  spam.offers@deals.top               YOU WON a free laptop!!               spam
  2026-11-24  neha.deshmukh@gmail.com             Can you review my pandas notebook     unread
* 2026-11-24  noreply@netlify.com                 Deploy failed for mediverse           unread,important
  2026-11-25  riya93@mitwpu.edu.in                Final deck draft attached             unread

=== counts ===
  total   : 11
  unread  : 6
  important: 3
  spam    : 1
  read    : 4

=== top senders ===
  coordinator@mitwpu.edu.in               2
  riya93@mitwpu.edu.in                    2
  noreply@netlify.com                     2
  aman_k99@sub.domain.co.in               1
  noreply@github.com                      1
  support@supabase.io                     1
  spam.offers@deals.top                   1
  neha.deshmukh@gmail.com                 1

=== domains ===
  mitwpu.edu.in             4
  netlify.com               2
  sub.domain.co.in          1
  github.com                1
  supabase.io               1
  deals.top                 1
  gmail.com                 1

=== needs a reply (unread and important) ===
  2026-11-20  coordinator@mitwpu.edu.in           Project review slot confirmed
  2026-11-23  coordinator@mitwpu.edu.in           Reminder: submit by 30 November
  2026-11-24  noreply@netlify.com                 Deploy failed for mediverse

=== emails per day ===
  2026-11-20  2  ##
  2026-11-21  2  ##
  2026-11-22  2  ##
  2026-11-23  2  ##
  2026-11-24  2  ##
  2026-11-25  1  #

=== wrote d:\Claude- Hospitalisation Services\python-lab-solutions\exp08\data\email_preview.txt ===
  Emails in archive: 11
  2026-11-20 | coordinator@mitwpu.edu.in | Project review slot confirmed | unread,important
  2026-11-20 | riya93@mitwpu.edu.in | Re: screenshots for the deck | read

  preview file: 3 line(s), 187 bytes

```

</details>

---

## Experiment 8 - Question 9: Survey Responses Handler

Scenario: survey_responses.txt contains responses to a survey question. Count
how many people responded and extract the first two responses into
sample_responses.txt.

Run: python q9_survey_responses_handler.py

**File:** [`q9_survey_responses_handler.py`](q9_survey_responses_handler.py) &nbsp;&middot;&nbsp; **Run:** `python q9_survey_responses_handler.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
"""
Experiment 8 - Question 9: Survey Responses Handler

Scenario: survey_responses.txt contains responses to a survey question. Count
how many people responded and extract the first two responses into
sample_responses.txt.

Run: python q9_survey_responses_handler.py
"""

import os
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
INPUT_FILE = os.path.join(DATA, "survey_responses.txt")
OUTPUT_FILE = os.path.join(DATA, "sample_responses.txt")

QUESTION = ("How likely are you to recommend the MediVerse bed-availability "
            "feature? (0-10, plus a comment)")

SAMPLE = """9 | Finding a free ICU bed used to take four phone calls. Now it is one screen.
8 | Useful, but the data looked stale once during the evening rush.
10 | Exactly what a district hospital needs. Shared it with two colleagues.
6 | Works, though the mobile layout squeezes the ward names.
7 | Good. Please add a filter for paediatric beds.
3 | It showed a bed as free that was already taken. Lost trust after that.
9 | The refresh is fast and the colour coding is clear.
10 | Our front desk now answers bed queries without calling the wards.
5 | Fine for one hospital, but we need a multi-hospital view.
8 | Solid. An SMS alert when ICU capacity drops below 10% would help.
2 | Could not log in for two days last week.
9 | Clean interface, no training needed for the staff.
7 | Decent, add a printable daily occupancy report.
10 | Best improvement to our workflow this year.
"""


def ensure_sample():
    os.makedirs(DATA, exist_ok=True)
    if not os.path.exists(INPUT_FILE):
        with open(INPUT_FILE, "w", encoding="utf-8") as fh:
            fh.write(SAMPLE)
        print(f"[setup] created sample input {INPUT_FILE}")


def nps_bucket(score):
    if score >= 9:
        return "promoter"
    if score >= 7:
        return "passive"
    return "detractor"


if __name__ == "__main__":
    ensure_sample()

    with open(INPUT_FILE, "r", encoding="utf-8") as fh:
        lines = [ln.rstrip("\n") for ln in fh if ln.strip()]

    print(f"=== survey question ===")
    print(f"  {QUESTION}")
    print(f"\n=== read {os.path.basename(INPUT_FILE)} ===")
    print(f"  people responded : {len(lines)}")
    print(f"  file size        : {os.path.getsize(INPUT_FILE)} bytes")

    responses = []
    for line in lines:
        score_text, _, comment = line.partition("|")
        try:
            responses.append((int(score_text.strip()), comment.strip()))
        except ValueError:
            responses.append((None, line.strip()))

    first_two = lines[:2]
    print("\n=== first two responses ===")
    for i, line in enumerate(first_two, 1):
        print(f"  {i}. {line}")

    scored = [(s, c) for s, c in responses if s is not None]
    scores = [s for s, _ in scored]

    print("\n=== score distribution ===")
    counts = Counter(scores)
    for score in range(11):
        n = counts.get(score, 0)
        if n:
            print(f"  {score:>2} : {'#' * n} ({n})")

    print("\n=== statistics ===")
    print(f"  responses with a score : {len(scored)}")
    print(f"  average score          : {sum(scores) / len(scores):.2f}")
    print(f"  highest / lowest       : {max(scores)} / {min(scores)}")
    srt = sorted(scores)
    mid = len(srt) // 2
    median = srt[mid] if len(srt) % 2 else (srt[mid - 1] + srt[mid]) / 2
    print(f"  median                 : {median}")

    buckets = Counter(nps_bucket(s) for s in scores)
    promoters = buckets.get("promoter", 0)
    detractors = buckets.get("detractor", 0)
    nps = (promoters - detractors) / len(scores) * 100

    print("\n=== net promoter breakdown ===")
    for name in ("promoter", "passive", "detractor"):
        n = buckets.get(name, 0)
        print(f"  {name:<11}{n:>3}  {n / len(scores) * 100:>5.1f}%")
    print(f"  NPS : {nps:+.1f}")

    print("\n=== detractor comments (act on these first) ===")
    for s, c in scored:
        if nps_bucket(s) == "detractor":
            print(f"  [{s}] {c}")

    print("\n=== feature requests mentioned ===")
    for s, c in scored:
        low = c.lower()
        if any(w in low for w in ("add", "please", "need", "would help")):
            print(f"  [{s}] {c}")

    words = Counter()
    for _, c in scored:
        words.update(w.strip(".,").lower() for w in c.split() if len(w) > 4)
    print("\n=== most mentioned terms ===")
    for word, n in words.most_common(6):
        print(f"  {word:<14}{n}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as fh:
        for line in first_two:
            fh.write(line + "\n")

    print(f"\n=== wrote {OUTPUT_FILE} ===")
    with open(OUTPUT_FILE, "r", encoding="utf-8") as fh:
        for i, line in enumerate(fh, 1):
            print(f"  {i}. {line.rstrip()}")
    print(f"\n  sample file: "
          f"{sum(1 for _ in open(OUTPUT_FILE, encoding='utf-8'))} of "
          f"{len(lines)} responses")
```

</details>

<details>
<summary>Program output</summary>

```text
=== survey question ===
  How likely are you to recommend the MediVerse bed-availability feature? (0-10, plus a comment)

=== read survey_responses.txt ===
  people responded : 14
  file size        : 885 bytes

=== first two responses ===
  1. 9 | Finding a free ICU bed used to take four phone calls. Now it is one screen.
  2. 8 | Useful, but the data looked stale once during the evening rush.

=== score distribution ===
   2 : # (1)
   3 : # (1)
   5 : # (1)
   6 : # (1)
   7 : ## (2)
   8 : ## (2)
   9 : ### (3)
  10 : ### (3)

=== statistics ===
  responses with a score : 14
  average score          : 7.36
  highest / lowest       : 10 / 2
  median                 : 8.0

=== net promoter breakdown ===
  promoter     6   42.9%
  passive      4   28.6%
  detractor    4   28.6%
  NPS : +14.3

=== detractor comments (act on these first) ===
  [6] Works, though the mobile layout squeezes the ward names.
  [3] It showed a bed as free that was already taken. Lost trust after that.
  [5] Fine for one hospital, but we need a multi-hospital view.
  [2] Could not log in for two days last week.

=== feature requests mentioned ===
  [10] Exactly what a district hospital needs. Shared it with two colleagues.
  [7] Good. Please add a filter for paediatric beds.
  [5] Fine for one hospital, but we need a multi-hospital view.
  [8] Solid. An SMS alert when ICU capacity drops below 10% would help.
  [9] Clean interface, no training needed for the staff.
  [7] Decent, add a printable daily occupancy report.

=== most mentioned terms ===
  hospital      2
  finding       1
  phone         1
  calls         1
  screen        1
  useful        1

=== wrote d:\Claude- Hospitalisation Services\python-lab-solutions\exp08\data\sample_responses.txt ===
  1. 9 | Finding a free ICU bed used to take four phone calls. Now it is one screen.
  2. 8 | Useful, but the data looked stale once during the evening rush.

  sample file: 2 of 14 responses

```

</details>

---

## Experiment 8 - Question 10: Book Chapter Processor

Scenario: eBook chapters are stored as text files (chapter1.txt). Count how
many lines the chapter has and extract the first two lines as a teaser, saving
the teaser in chapter_teaser.txt.

Run: python q10_book_chapter_processor.py

**File:** [`q10_book_chapter_processor.py`](q10_book_chapter_processor.py) &nbsp;&middot;&nbsp; **Run:** `python q10_book_chapter_processor.py` &nbsp;&middot;&nbsp; **Status:** ran successfully

<details open>
<summary>Solution code</summary>

```python
"""
Experiment 8 - Question 10: Book Chapter Processor

Scenario: eBook chapters are stored as text files (chapter1.txt). Count how
many lines the chapter has and extract the first two lines as a teaser, saving
the teaser in chapter_teaser.txt.

Run: python q10_book_chapter_processor.py
"""

import os
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
INPUT_FILE = os.path.join(DATA, "chapter1.txt")
OUTPUT_FILE = os.path.join(DATA, "chapter_teaser.txt")

SAMPLE = """Chapter 1: The Ward at Midnight
The corridor lights of the district hospital never fully went out.
Dr. Kavita Rao walked the length of Ward C with a clipboard she no longer
needed, because the numbers she wanted were already on the screen in her
pocket.
Three years earlier, finding a free bed meant four phone calls and a guess.
The night nurse would shout across the corridor, someone would check a
register, and a patient on a trolley would wait.
Tonight the dashboard said eleven beds free in Ward C and two in the ICU,
and it had said so within thirty seconds of the last discharge.
She stopped at the nurses' station.
"Anything from the taluka hospital?" she asked.
"Two transfers," the nurse said, not looking up. "They checked availability
before dispatching. First time that has happened."
Kavita wrote nothing down.
The system had not cured anybody. It had only removed the waiting that came
from not knowing, which, she had come to believe, was its own kind of illness.
Outside, an ambulance turned in without its siren, which meant there was time.
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

    text = "\n".join(lines)
    words = text.split()
    sentences = [s.strip() for s in text.replace("!", ".").replace("?", ".")
                 .split(".") if s.strip()]

    print(f"=== read {os.path.basename(INPUT_FILE)} ===")
    print(f"  lines in the chapter : {len(lines)}")
    print(f"  non-empty lines      : {sum(1 for ln in lines if ln.strip())}")
    print(f"  words                : {len(words)}")
    print(f"  characters           : {len(text)}")
    print(f"  sentences            : {len(sentences)}")
    print(f"  file size            : {os.path.getsize(INPUT_FILE)} bytes")

    first_two = lines[:2]
    print("\n=== teaser: the first two lines ===")
    for i, line in enumerate(first_two, 1):
        print(f"  {i}. {line}")

    print("\n=== reading metrics ===")
    print(f"  average words per sentence : {len(words) / len(sentences):.1f}")
    print(f"  average word length        : "
          f"{sum(len(w.strip('.,\"')) for w in words) / len(words):.2f} chars")
    print(f"  estimated reading time     : "
          f"{len(words) / 200:.1f} minute(s) at 200 wpm")

    print("\n=== dialogue lines ===")
    for n, line in enumerate(lines, 1):
        if '"' in line:
            print(f"  line {n:>2}: {line.strip()[:70]}")

    stop = {"the", "and", "that", "with", "which", "from", "what", "than",
            "they", "have", "been", "were", "would", "there", "because",
            "before", "only", "said", "came", "into", "without", "already"}
    freq = Counter(w.strip('.,"\'').lower() for w in words
                   if len(w) > 3 and w.strip('.,"\'').lower() not in stop)
    print("\n=== most frequent content words ===")
    for word, n in freq.most_common(8):
        print(f"  {word:<14}{n}")

    print("\n=== longest lines ===")
    for n, line in sorted(enumerate(lines, 1), key=lambda p: -len(p[1]))[:3]:
        print(f"  line {n:>2} ({len(line)} chars): {line[:60]}...")

    print("\n=== chapter title detected ===")
    print(f"  {lines[0] if lines[0].lower().startswith('chapter') else '(none)'}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as fh:
        for line in first_two:
            fh.write(line + "\n")

    print(f"\n=== wrote {OUTPUT_FILE} ===")
    with open(OUTPUT_FILE, "r", encoding="utf-8") as fh:
        teaser = fh.read()
    for i, line in enumerate(teaser.splitlines(), 1):
        print(f"  {i}. {line}")

    print(f"\n  teaser   : {len(teaser.split())} words, "
          f"{os.path.getsize(OUTPUT_FILE)} bytes")
    print(f"  chapter  : {len(words)} words, "
          f"{os.path.getsize(INPUT_FILE)} bytes")
    print(f"  the teaser is "
          f"{len(teaser.split()) / len(words) * 100:.1f}% of the chapter")
```

</details>

<details>
<summary>Program output</summary>

```text
=== read chapter1.txt ===
  lines in the chapter : 18
  non-empty lines      : 18
  words                : 185
  characters           : 1059
  sentences            : 16
  file size            : 1078 bytes

=== teaser: the first two lines ===
  1. Chapter 1: The Ward at Midnight
  2. The corridor lights of the district hospital never fully went out.

=== reading metrics ===
  average words per sentence : 11.6
  average word length        : 4.55 chars
  estimated reading time     : 0.9 minute(s) at 200 wpm

=== dialogue lines ===
  line 12: "Anything from the taluka hospital?" she asked.
  line 13: "Two transfers," the nurse said, not looking up. "They checked availab
  line 14: before dispatching. First time that has happened."

=== most frequent content words ===
  ward          3
  corridor      2
  kavita        2
  free          2
  meant         2
  nurse         2
  time          2
  chapter       1

=== longest lines ===
  line 17 (78 chars): from not knowing, which, she had come to believe, was its ow...
  line 18 (78 chars): Outside, an ambulance turned in without its siren, which mea...
  line  6 (75 chars): Three years earlier, finding a free bed meant four phone cal...

=== chapter title detected ===
  Chapter 1: The Ward at Midnight

=== wrote d:\Claude- Hospitalisation Services\python-lab-solutions\exp08\data\chapter_teaser.txt ===
  1. Chapter 1: The Ward at Midnight
  2. The corridor lights of the district hospital never fully went out.

  teaser   : 17 words, 101 bytes
  chapter  : 185 words, 1078 bytes
  the teaser is 9.2% of the chapter

```

</details>

---
