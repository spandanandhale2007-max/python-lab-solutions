"""
Experiment 2 - Question 9: Temperature Conversion Closure

Scenario: A closure that generates a function converting Celsius to Fahrenheit
and vice versa, based on user input.

Rubrics covered:
  * closure with internal state
  * converts in both directions
  * a separate closure for each direction
  * clean function design
"""


def make_converter(direction, precision=2):
    """Factory returning a closure. direction, precision and the call counter
    stay alive in the enclosing scope after make_converter has returned."""

    direction = direction.upper()
    if direction not in ("C2F", "F2C"):
        raise ValueError("direction must be 'C2F' or 'F2C'")

    calls = 0                 # internal state captured by the closure

    def convert(value):
        nonlocal calls
        calls += 1
        if direction == "C2F":
            result = value * 9 / 5 + 32
            label = f"{value} C = {round(result, precision)} F"
        else:
            result = (value - 32) * 5 / 9
            label = f"{value} F = {round(result, precision)} C"
        print(f"  [{direction} call #{calls}] {label}")
        return round(result, precision)

    def usage():
        return calls

    convert.usage = usage      # expose the captured counter
    convert.direction = direction
    return convert


def make_scaled_converter(factor, offset, unit_in, unit_out):
    """Generic closure: any linear unit conversion."""
    def convert(value):
        return round(value * factor + offset, 2)
    convert.__doc__ = f"{unit_in} -> {unit_out}"
    return convert


if __name__ == "__main__":
    c_to_f = make_converter("C2F")
    f_to_c = make_converter("F2C")

    print("=== two independent closures, two separate states ===")
    for c in (0, 37, 100, -40):
        c_to_f(c)
    for f in (32, 98.6, 212, -40):
        f_to_c(f)

    print(f"\n  c_to_f was used {c_to_f.usage()} times")
    print(f"  f_to_c was used {f_to_c.usage()} times  (counters are separate)")

    print("\n=== round trip proves both directions agree ===")
    original = 36.6
    there = c_to_f(original)
    back = f_to_c(there)
    print(f"  {original} C -> {there} F -> {back} C")

    print("\n=== the captured variables live in the closure cell ===")
    print("  free variables:", c_to_f.__code__.co_freevars)
    print("  cell contents :", [cell.cell_contents for cell in c_to_f.__closure__])

    print("\n=== generic closure factory ===")
    k_from_c = make_scaled_converter(1, 273.15, "Celsius", "Kelvin")
    mi_from_km = make_scaled_converter(0.621371, 0, "km", "miles")
    print("  25 C in Kelvin :", k_from_c(25))
    print("  100 km in miles:", mi_from_km(100))

    print("\n=== user input (falls back to a demo value) ===")
    try:
        choice = input("Convert [1] C->F or [2] F->C : ").strip()
        value = float(input("Enter the temperature: ").strip())
    except (EOFError, ValueError, OSError):
        choice, value = "1", 42.0
        print(f"  (no input - demonstrating with {value} C)")
    (c_to_f if choice != "2" else f_to_c)(value)
