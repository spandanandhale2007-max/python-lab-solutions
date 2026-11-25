"""
Experiment 1 - Question 6: Car vs ElectricCar

Scenario: A car showroom simulation. Class Car has properties like fuel type;
ElectricCar overrides behaviour to simulate electric-specific features.

Rubrics covered:
  * inheritance and method overriding
  * refuel() differs in base vs derived class
  * constructor reuse with super()
  * realistic attributes and methods
"""


class Car:
    def __init__(self, brand, model, price, fuel_type="Petrol",
                 tank_capacity=40, mileage=18.0):
        self.brand = brand
        self.model = model
        self.price = price
        self.fuel_type = fuel_type
        self.tank_capacity = tank_capacity     # litres
        self.mileage = mileage                 # km per litre
        self.fuel_level = 0.0
        self.odometer = 0.0

    def refuel(self, litres):
        space = self.tank_capacity - self.fuel_level
        added = min(litres, space)
        self.fuel_level += added
        print(f"[{self.model}] Pumped {added:.1f} L of {self.fuel_type}. "
              f"Tank {self.fuel_level:.1f}/{self.tank_capacity} L")
        if added < litres:
            print(f"   (tank full, {litres - added:.1f} L not taken)")

    def range_left(self):
        return self.fuel_level * self.mileage

    def drive(self, km):
        if km > self.range_left():
            print(f"[{self.model}] Cannot drive {km} km, range is only "
                  f"{self.range_left():.0f} km")
            return False
        self.fuel_level -= km / self.mileage
        self.odometer += km
        print(f"[{self.model}] Drove {km} km. Range left {self.range_left():.0f} km")
        return True

    def running_cost_per_km(self, fuel_price=106.0):
        return fuel_price / self.mileage

    def __str__(self):
        return (f"{self.brand} {self.model} | {self.fuel_type} | "
                f"Rs.{self.price:,} | {self.mileage} km/L | "
                f"odo {self.odometer:.0f} km")


class ElectricCar(Car):
    def __init__(self, brand, model, price, battery_kwh, km_per_kwh,
                 charger_kw=7.2):
        # constructor reuse: tank_capacity -> battery kWh, mileage -> km per kWh
        super().__init__(brand, model, price, fuel_type="Electric",
                         tank_capacity=battery_kwh, mileage=km_per_kwh)
        self.battery_kwh = battery_kwh
        self.charger_kw = charger_kw

    def battery_percent(self):
        return 100.0 * self.fuel_level / self.battery_kwh

    # --- overridden behaviour ---
    def refuel(self, kwh):
        space = self.battery_kwh - self.fuel_level
        added = min(kwh, space)
        self.fuel_level += added
        hours = added / self.charger_kw
        print(f"[{self.model}] Charged {added:.1f} kWh in {hours:.1f} h on a "
              f"{self.charger_kw} kW charger. Battery {self.battery_percent():.0f}%")
        if added < kwh:
            print(f"   (battery full, {kwh - added:.1f} kWh not taken)")

    def running_cost_per_km(self, unit_price=9.0):
        return unit_price / self.mileage

    def __str__(self):
        return (f"{self.brand} {self.model} | Electric | Rs.{self.price:,} | "
                f"{self.battery_kwh} kWh | {self.mileage} km/kWh | "
                f"battery {self.battery_percent():.0f}% | odo {self.odometer:.0f} km")


if __name__ == "__main__":
    showroom = [
        Car("Maruti", "Swift VXi", 799000, tank_capacity=37, mileage=22.4),
        ElectricCar("Tata", "Nexon EV", 1499000, battery_kwh=40.5, km_per_kwh=7.0),
    ]

    print("=== Showroom stock ===")
    for c in showroom:
        print(" ", c)

    print("\n=== refuel() resolves differently for each class ===")
    for c in showroom:
        c.refuel(20)

    print("\n=== same drive() inherited by both ===")
    for c in showroom:
        c.drive(120)

    print("\n=== running cost comparison ===")
    for c in showroom:
        print(f"  {c.model:<12} Rs.{c.running_cost_per_km():.2f} per km")

    print("\n=== final state ===")
    for c in showroom:
        print(" ", c)

    print("\nElectricCar is a Car:", isinstance(showroom[1], Car))
    print("MRO:", [k.__name__ for k in ElectricCar.__mro__])
