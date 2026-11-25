"""
Experiment 2 - Question 8: Email Filter with Iterator

Scenario: A custom iterator that walks a list of strings and yields only the
valid email addresses.

Rubrics covered:
  * __iter__ and __next__ implemented
  * email validated during iteration
  * StopIteration raised when the list ends
  * all valid emails printed
"""

import re

EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+\.[A-Za-z]{2,}$")


class EmailFilterIterator:
    """Custom iterator: skips invalid entries instead of returning them."""

    def __init__(self, items):
        self.items = list(items)
        self.index = 0
        self.checked = 0
        self.skipped = 0

    def __iter__(self):
        return self                       # the iterator is its own iterable

    def __next__(self):
        while self.index < len(self.items):
            candidate = str(self.items[self.index]).strip()
            self.index += 1
            self.checked += 1
            if EMAIL_RE.match(candidate):
                return candidate.lower()
            self.skipped += 1
        raise StopIteration               # list exhausted

    def reset(self):
        self.index = self.checked = self.skipped = 0


class Mailbox:
    """Iterable container: a fresh iterator is produced on every for-loop."""

    def __init__(self, raw_lines):
        self.raw_lines = raw_lines

    def __iter__(self):
        return EmailFilterIterator(self.raw_lines)

    def __len__(self):
        return len(self.raw_lines)


if __name__ == "__main__":
    raw = [
        "spandan@example.com",
        "not-an-email",
        "riya.sharma@mitwpu.edu.in",
        "@missinglocal.com",
        "  AMAN_K99@Sub.Domain.CO  ",
        "user@nodot",
        "neha+promo@gmail.com",
        12345,
        "double@@at.com",
        "last.valid@zoho.in",
    ]

    print("=== iterating with a for loop ===")
    it = EmailFilterIterator(raw)
    for email in it:
        print("  valid ->", email)
    print(f"  checked {it.checked}, skipped {it.skipped}")

    print("\n=== manual next() until StopIteration ===")
    it2 = EmailFilterIterator(raw)
    while True:
        try:
            print("  next():", next(it2))
        except StopIteration:
            print("  StopIteration raised - list ended")
            break

    print("\n=== reusable iterable container ===")
    box = Mailbox(raw)
    print("  pass 1:", list(box))
    print("  pass 2:", list(box), "(a new iterator each time)")
    print(f"  {len(list(box))} valid out of {len(box)} raw lines")

    print("\n=== collected list of valid emails ===")
    for i, e in enumerate(Mailbox(raw), 1):
        print(f"  {i}. {e}")
