"""
Experiment 2 - Question 10: Retry Logic with Decorators

Scenario: Decorate a function that simulates an API call so it retries on
failure (failures are generated randomly).

Rubrics covered:
  * retry mechanism inside a decorator
  * try/except used
  * random failures simulated
  * retries capped by a limit
"""

import functools
import random
import time


class APIError(Exception):
    """Simulated transient server error."""


def retry(times=3, delay=0.2, backoff=2.0, exceptions=(APIError,)):
    """Parameterised decorator: retries the call up to `times` attempts with
    an exponentially growing delay, then re-raises the last error."""

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            wait = delay
            last_error = None
            for attempt in range(1, times + 1):
                try:
                    result = func(*args, **kwargs)
                    if attempt > 1:
                        print(f"   -> succeeded on attempt {attempt}/{times}")
                    return result
                except exceptions as exc:
                    last_error = exc
                    print(f"   attempt {attempt}/{times} failed: "
                          f"{type(exc).__name__}: {exc}")
                    if attempt < times:
                        print(f"   retrying in {wait:.2f}s ...")
                        time.sleep(wait)
                        wait *= backoff
            print(f"   -> giving up after {times} attempts")
            raise last_error
        wrapper.max_attempts = times
        return wrapper
    return decorator


# ---------------- simulated flaky services ----------------
@retry(times=5, delay=0.1)
def fetch_user_profile(user_id, failure_rate=0.6):
    """Fails randomly, like a real network call."""
    if random.random() < failure_rate:
        raise APIError(f"504 gateway timeout for user {user_id}")
    return {"id": user_id, "name": "Spandan Andhale", "plan": "student"}


@retry(times=3, delay=0.05)
def charge_payment(amount, failure_rate=1.0):
    """Always fails, to show the retry limit being reached."""
    if random.random() < failure_rate:
        raise APIError(f"payment gateway refused Rs.{amount}")
    return f"charged Rs.{amount}"


@retry(times=4, delay=0.05, exceptions=(APIError, ConnectionError))
def upload_report(name):
    roll = random.random()
    if roll < 0.3:
        raise ConnectionError("DNS lookup failed")
    if roll < 0.6:
        raise APIError("413 payload too large")
    return f"{name} uploaded"


if __name__ == "__main__":
    random.seed(7)            # reproducible run for the lab record

    print("=== 1. flaky GET, succeeds within the retry budget ===")
    try:
        print("  result:", fetch_user_profile(42))
    except APIError as e:
        print("  final failure:", e)

    print("\n=== 2. permanent failure, retry limit enforced ===")
    try:
        charge_payment(1999)
    except APIError as e:
        print("  caller sees:", type(e).__name__, "-", e)

    print("\n=== 3. retrying more than one exception type ===")
    try:
        print("  result:", upload_report("marks.csv"))
    except (APIError, ConnectionError) as e:
        print("  final failure:", type(e).__name__, "-", e)

    print("\n=== decorator metadata ===")
    print("  fetch_user_profile.__name__       :", fetch_user_profile.__name__)
    print("  fetch_user_profile.max_attempts   :", fetch_user_profile.max_attempts)
    print("  charge_payment.max_attempts       :", charge_payment.max_attempts)

    print("\n=== success rate over 10 independent calls ===")
    ok = 0
    for i in range(10):
        try:
            fetch_user_profile(i, failure_rate=0.5)
            ok += 1
        except APIError:
            pass
    print(f"  {ok}/10 calls eventually succeeded thanks to retries")
