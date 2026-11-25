"""
Experiment 2 - Question 6: Function Logger Decorator

Scenario: A decorator that logs the function name, input and output every time
a function is called (for auditing).

Rubrics covered:
  * @decorator syntax used
  * arguments and return values captured
  * timestamp included
  * applied to multiple functions
"""

import functools
import time
from datetime import datetime

AUDIT_TRAIL = []


def audit_log(func):
    """Logs name, args, kwargs, return value, duration and a timestamp."""

    @functools.wraps(func)                 # keeps __name__, __doc__ intact
    def wrapper(*args, **kwargs):
        stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        shown_args = ", ".join(repr(a) for a in args)
        shown_kwargs = ", ".join(f"{k}={v!r}" for k, v in kwargs.items())
        signature = ", ".join(p for p in (shown_args, shown_kwargs) if p)

        start = time.perf_counter()
        try:
            result = func(*args, **kwargs)
        except Exception as exc:
            elapsed = (time.perf_counter() - start) * 1000
            line = (f"[{stamp}] CALL {func.__name__}({signature}) "
                    f"RAISED {type(exc).__name__}: {exc} ({elapsed:.2f} ms)")
            print(line)
            AUDIT_TRAIL.append(line)
            raise
        elapsed = (time.perf_counter() - start) * 1000
        line = (f"[{stamp}] CALL {func.__name__}({signature}) "
                f"-> {result!r} ({elapsed:.2f} ms)")
        print(line)
        AUDIT_TRAIL.append(line)
        return result

    return wrapper


# ---------------- applied to several functions ----------------
@audit_log
def add(a, b):
    """Adds two numbers."""
    return a + b


@audit_log
def apply_gst(amount, rate=18):
    return round(amount * (1 + rate / 100), 2)


@audit_log
def grade(marks):
    if not 0 <= marks <= 100:
        raise ValueError("marks must be between 0 and 100")
    return "A" if marks >= 80 else "B" if marks >= 60 else "C"


@audit_log
def slow_square(n):
    time.sleep(0.05)
    return n * n


if __name__ == "__main__":
    print("=== audited calls ===")
    add(12, 30)
    apply_gst(1500)
    apply_gst(2000, rate=5)
    grade(88)
    slow_square(9)

    print("\n=== an exception is also audited ===")
    try:
        grade(140)
    except ValueError as e:
        print("  caught by caller:", e)

    print("\n=== metadata preserved by functools.wraps ===")
    print("  add.__name__ :", add.__name__)
    print("  add.__doc__  :", add.__doc__)

    print(f"\n=== audit trail ({len(AUDIT_TRAIL)} entries) ===")
    for line in AUDIT_TRAIL:
        print("  ", line)
