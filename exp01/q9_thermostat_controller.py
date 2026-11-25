"""
Experiment 1 - Question 9: Thermostat Controller

Scenario: A smart thermostat keeps a room between 18 C and 30 C. It must not
allow values outside the allowed range.

Rubrics covered:
  * encapsulation with validation in the setter
  * feedback on invalid input
  * current status shown via __str__
  * private temperature variable
"""


class Thermostat:
    MIN_TEMP = 18.0
    MAX_TEMP = 30.0

    def __init__(self, room, target=24.0):
        self.room = room
        self.__temperature = None        # private
        self.__history = []
        self.set_temperature(target)

    # ---- controlled access ----
    @property
    def temperature(self):
        return self.__temperature

    @temperature.setter
    def temperature(self, value):
        self.set_temperature(value)

    def set_temperature(self, value):
        try:
            value = float(value)
        except (TypeError, ValueError):
            print(f"REJECTED: '{value}' is not a number. Temperature unchanged "
                  f"at {self.__temperature} C")
            return False
        if value < Thermostat.MIN_TEMP:
            print(f"REJECTED: {value} C is below the minimum "
                  f"{Thermostat.MIN_TEMP} C. Request ignored.")
            return False
        if value > Thermostat.MAX_TEMP:
            print(f"REJECTED: {value} C is above the maximum "
                  f"{Thermostat.MAX_TEMP} C. Request ignored.")
            return False
        self.__temperature = value
        self.__history.append(value)
        print(f"ACCEPTED: {self.room} target set to {value} C")
        return True

    def warmer(self, step=1.0):
        return self.set_temperature((self.__temperature or 0) + step)

    def cooler(self, step=1.0):
        return self.set_temperature((self.__temperature or 0) - step)

    def mode(self):
        if self.__temperature <= 20:
            return "HEATING"
        if self.__temperature >= 28:
            return "COOLING"
        return "IDLE"

    def history(self):
        return list(self.__history)

    def __str__(self):
        span = self.MAX_TEMP - self.MIN_TEMP
        pos = int((self.__temperature - self.MIN_TEMP) / span * 20)
        bar = "=" * pos + "o" + "-" * (20 - pos)
        return (f"[{self.room}] {self.__temperature:.1f} C  |{bar}|  "
                f"mode={self.mode()}  range {self.MIN_TEMP}-{self.MAX_TEMP} C")


if __name__ == "__main__":
    t = Thermostat("Bedroom", 24)
    print(t)

    print("\n--- valid adjustments ---")
    t.warmer(3)
    print(t)
    t.cooler(5)
    print(t)

    print("\n--- invalid adjustments get feedback, state is protected ---")
    t.set_temperature(45)
    t.set_temperature(5)
    t.set_temperature("hot")
    t.temperature = 99          # goes through the property setter -> rejected
    print(t)

    print("\n--- boundaries are allowed ---")
    t.set_temperature(18)
    t.set_temperature(30)
    print(t)

    print("\nPrivate attribute is name-mangled, not directly reachable:")
    print("  'temperature' in instance dict:", "temperature" in t.__dict__)
    print("  stored as:", [k for k in t.__dict__ if "temperature" in k])
    print("  accepted history:", t.history())
