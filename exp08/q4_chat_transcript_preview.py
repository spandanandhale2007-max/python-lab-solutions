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
