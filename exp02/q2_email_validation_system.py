"""
Experiment 2 - Question 2: Email Validation System

Scenario: A class stores valid email addresses. The system rejects and does not
store invalid formats (missing '@', missing domain, and so on).

Rubrics covered:
  * static methods used for validation
  * a list of emails is taken as input and filtered
  * only valid addresses are stored
  * the valid email list is printed
"""

import re


class EmailBook:
    PATTERN = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}$")

    def __init__(self, owner):
        self.owner = owner
        self.valid = []
        self.rejected = []

    # ---------- static validation helpers ----------
    @staticmethod
    def is_valid(email):
        if not isinstance(email, str):
            return False
        email = email.strip()
        if email.count("@") != 1:
            return False
        if ".." in email or email.startswith(".") or email.endswith("."):
            return False
        return bool(EmailBook.PATTERN.match(email))

    @staticmethod
    def reason(email):
        e = (email or "").strip()
        if not e:
            return "empty string"
        if e.count("@") == 0:
            return "missing '@'"
        if e.count("@") > 1:
            return "more than one '@'"
        local, _, domain = e.partition("@")
        if not local:
            return "missing local part"
        if not domain:
            return "missing domain"
        if "." not in domain:
            return "domain has no dot / no TLD"
        if len(domain.rsplit(".", 1)[1]) < 2:
            return "TLD too short"
        if " " in e:
            return "contains a space"
        return "does not match the allowed character pattern"

    @staticmethod
    def normalise(email):
        return email.strip().lower()

    # ---------- storage ----------
    def add(self, email):
        if EmailBook.is_valid(email):
            clean = EmailBook.normalise(email)
            if clean in self.valid:
                self.rejected.append((email, "duplicate"))
                return False
            self.valid.append(clean)
            return True
        self.rejected.append((email, EmailBook.reason(email)))
        return False

    def add_many(self, emails):
        return sum(self.add(e) for e in emails)

    def report(self):
        print(f"\n=== {self.owner}: {len(self.valid)} stored address(es) ===")
        for i, e in enumerate(self.valid, 1):
            print(f"  {i}. {e}")
        print(f"\n=== {len(self.rejected)} rejected ===")
        for e, why in self.rejected:
            print(f"  {str(e)!r:<32} -> {why}")


if __name__ == "__main__":
    raw_input_list = [
        "spandanandhale@example.com",
        "riya.sharma+college@mitwpu.edu.in",
        "plainaddress",                 # no @
        "no-at-sign.com",               # no @
        "two@@signs.com",               # two @
        "@nolocalpart.com",             # no local part
        "missingdomain@",               # no domain
        "user@nodot",                   # no TLD
        "user@short.c",                 # TLD too short
        "has space@mail.com",           # space
        "aman_k99@sub.domain.co.in",
        "SPANDANANDHALE@EXAMPLE.COM",   # duplicate after normalising
    ]

    book = EmailBook("Newsletter subscribers")
    stored = book.add_many(raw_input_list)

    print(f"Processed {len(raw_input_list)} entries, stored {stored}.")
    book.report()

    print("\n=== static method can be used without an instance ===")
    for probe in ("abc@def.com", "abc@def"):
        print(f"  EmailBook.is_valid({probe!r}) -> {EmailBook.is_valid(probe)}")
