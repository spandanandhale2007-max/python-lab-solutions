"""
Experiment 3 - Question 8: Vehicle Factory

Scenario: A rental service that returns different vehicle classes from a
factory based on the type requested (Bike, Car, Truck).

Rubrics covered:
  * factory returns the appropriate object
  * polymorphic rent() method
  * clean vehicle hierarchy
  * easy future expansion
"""

from abc import ABC, abstractmethod


class Vehicle(ABC):
    wheels = 0
    licence_required = "LMV"

    def __init__(self, model, reg_no, daily_rate):
        self.model = model
        self.reg_no = reg_no
        self.daily_rate = daily_rate
        self.rented_to = None

    @abstractmethod
    def rent(self, customer, days):
        ...

    def is_available(self):
        return self.rented_to is None

    def base_cost(self, days):
        return self.daily_rate * days

    def return_vehicle(self):
        if self.rented_to is None:
            print(f"  {self.model} was not rented out")
            return False
        print(f"  {self.model} returned by {self.rented_to}")
        self.rented_to = None
        return True

    def __str__(self):
        state = "available" if self.is_available() else f"with {self.rented_to}"
        return (f"{type(self).__name__:<6} {self.model:<16} {self.reg_no:<12} "
                f"{self.wheels} wheels  Rs.{self.daily_rate:>5}/day  [{state}]")


class Bike(Vehicle):
    wheels = 2
    licence_required = "MCWG"

    def __init__(self, model, reg_no, daily_rate=399, helmets=2):
        super().__init__(model, reg_no, daily_rate)
        self.helmets = helmets

    def rent(self, customer, days):
        if not self.is_available():
            print(f"  {self.model} is already rented")
            return None
        cost = self.base_cost(days)
        self.rented_to = customer
        print(f"  BIKE  : {self.model} to {customer} for {days} day(s) "
              f"= Rs.{cost:,.0f} (+{self.helmets} helmets, "
              f"{self.licence_required} licence)")
        return cost


class Car(Vehicle):
    wheels = 4

    def __init__(self, model, reg_no, daily_rate=2199, seats=5, ac=True):
        super().__init__(model, reg_no, daily_rate)
        self.seats = seats
        self.ac = ac

    def rent(self, customer, days):
        if not self.is_available():
            print(f"  {self.model} is already rented")
            return None
        cost = self.base_cost(days)
        if days >= 7:
            cost *= 0.9                    # weekly discount
        self.rented_to = customer
        print(f"  CAR   : {self.model} to {customer} for {days} day(s) "
              f"= Rs.{cost:,.0f} ({self.seats} seats, "
              f"{'AC' if self.ac else 'non-AC'})")
        return cost


class Truck(Vehicle):
    wheels = 6
    licence_required = "HMV"

    def __init__(self, model, reg_no, daily_rate=4999, payload_tonnes=9):
        super().__init__(model, reg_no, daily_rate)
        self.payload_tonnes = payload_tonnes

    def rent(self, customer, days):
        if not self.is_available():
            print(f"  {self.model} is already rented")
            return None
        cost = self.base_cost(days) + 1500          # loading charge
        self.rented_to = customer
        print(f"  TRUCK : {self.model} to {customer} for {days} day(s) "
              f"= Rs.{cost:,.0f} (payload {self.payload_tonnes} t, "
              f"{self.licence_required} licence, Rs.1,500 loading)")
        return cost


class VehicleFactory:
    _catalogue = {
        "bike": (Bike, ("Royal Enfield Classic 350", "MH12-AB-1234")),
        "car": (Car, ("Hyundai Creta", "MH12-CD-5678")),
        "truck": (Truck, ("Tata LPT 1109", "MH12-EF-9012")),
    }

    @classmethod
    def create(cls, kind, **overrides):
        key = kind.strip().lower()
        if key not in cls._catalogue:
            raise ValueError(f"we do not rent {kind!r}; available: "
                             f"{', '.join(sorted(cls._catalogue))}")
        klass, defaults = cls._catalogue[key]
        model, reg = overrides.pop("model", defaults[0]), \
            overrides.pop("reg_no", defaults[1])
        return klass(model, reg, **overrides)

    @classmethod
    def register(cls, kind, klass, defaults):
        cls._catalogue[kind] = (klass, defaults)
        print(f"[factory] new vehicle type available: {kind}")

    @classmethod
    def types(cls):
        return sorted(cls._catalogue)


if __name__ == "__main__":
    print("rentable types:", VehicleFactory.types())

    print("\n=== the factory decides the class ===")
    fleet = [VehicleFactory.create(k) for k in ("bike", "car", "truck")]
    for v in fleet:
        print("  create ->", type(v).__name__, "|", v)

    print("\n=== polymorphic rent() through one loop ===")
    total = 0
    for v, customer, days in zip(fleet, ("Spandan", "Riya", "Shree Logistics"),
                                 (2, 8, 3)):
        amount = v.rent(customer, days)
        total += amount or 0
    print(f"  revenue booked: Rs.{total:,.0f}")

    print("\n=== double rent and return ===")
    fleet[0].rent("Aman", 1)
    fleet[0].return_vehicle()
    fleet[0].rent("Aman", 1)

    print("\n=== unknown type ===")
    try:
        VehicleFactory.create("helicopter")
    except ValueError as e:
        print("  ", e)

    print("\n=== extending the fleet later ===")
    class EScooter(Vehicle):
        wheels = 2
        licence_required = "none"

        def rent(self, customer, days):
            cost = self.base_cost(days)
            self.rented_to = customer
            print(f"  ESCOOT: {self.model} to {customer} for {days} day(s) "
                  f"= Rs.{cost:,.0f} (no licence needed)")
            return cost

    VehicleFactory.register("escooter", EScooter, ("Ather 450X", "MH12-GH-3456"))
    VehicleFactory.create("escooter", daily_rate=299).rent("Neha", 4)
    print("  rentable types now:", VehicleFactory.types())

    print("\n=== final fleet state ===")
    for v in fleet:
        print("  ", v)
