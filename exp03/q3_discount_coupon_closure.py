"""
Experiment 3 - Question 3: Discount Coupon Closure

Scenario: Generate discount functions using closures (10%, 20% and so on).

Rubrics covered:
  * closure returns a discount function
  * applied to different item prices
  * multiple closures with different rates
  * final price after discount printed
"""


def make_coupon(code, percent, max_discount=None, min_order=0):
    """Returns a closure that remembers code, percent, caps and a usage count."""

    uses = 0

    def apply(price):
        nonlocal uses
        if price < min_order:
            print(f"  {code:<10} not valid: order Rs.{price:,.2f} is below the "
                  f"minimum Rs.{min_order:,.2f}")
            return price
        discount = price * percent / 100
        if max_discount is not None:
            discount = min(discount, max_discount)
        uses += 1
        final = price - discount
        print(f"  {code:<10} {percent:>2}% off Rs.{price:>9,.2f} -> "
              f"saved Rs.{discount:>8,.2f}  pay Rs.{final:>9,.2f}")
        return round(final, 2)

    apply.code = code
    apply.percent = percent
    apply.uses = lambda: uses
    return apply


def make_flat_coupon(code, amount, min_order=0):
    def apply(price):
        if price < min_order:
            print(f"  {code:<10} needs a minimum order of Rs.{min_order:,.2f}")
            return price
        final = max(0.0, price - amount)
        print(f"  {code:<10} flat Rs.{amount} off Rs.{price:,.2f} -> "
              f"pay Rs.{final:,.2f}")
        return round(final, 2)
    apply.code = code
    return apply


def best_offer(price, coupons):
    """Picks the coupon that gives the lowest final price."""
    quiet = []
    for c in coupons:
        import io
        import contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            quiet.append((c(price), c.code))
    return min(quiet)


if __name__ == "__main__":
    # several independent closures, each with its own captured rate
    save10 = make_coupon("SAVE10", 10)
    save20 = make_coupon("SAVE20", 20, max_discount=500)
    festive30 = make_coupon("FESTIVE30", 30, max_discount=1500, min_order=2000)
    flat250 = make_flat_coupon("FLAT250", 250, min_order=999)

    prices = [499.00, 1899.00, 7499.00]

    for p in prices:
        print(f"\n=== cart value Rs.{p:,.2f} ===")
        for coupon in (save10, save20, festive30, flat250):
            coupon(p)

    print("\n=== each closure keeps its own usage counter ===")
    for coupon in (save10, save20, festive30):
        print(f"  {coupon.code:<10} used {coupon.uses()} time(s) "
              f"at {coupon.percent}%")

    print("\n=== closure internals ===")
    print("  free variables:", save20.__code__.co_freevars)
    print("  captured cells:", [c.cell_contents for c in save20.__closure__])

    print("\n=== best automatic offer per cart ===")
    for p in prices:
        final, code = best_offer(p, [save10, save20, festive30, flat250])
        print(f"  Rs.{p:>9,.2f} -> best is {code:<10} final Rs.{final:,.2f}")

    print("\n=== building coupons in a loop (late binding avoided) ===")
    tiered = [make_coupon(f"TIER{r}", r) for r in (5, 15, 25)]
    for t in tiered:
        t(1000)
