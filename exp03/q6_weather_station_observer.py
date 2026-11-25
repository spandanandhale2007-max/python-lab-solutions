"""
Experiment 3 - Question 6: Weather Station Observer

Scenario: A weather station where multiple displays update the temperature
whenever the sensor changes.

Rubrics covered:
  * observer pattern with subscribe / unsubscribe
  * all observers notified on change
  * sensor decoupled from the displays
  * updated data printed for each display
"""

from abc import ABC, abstractmethod


class Observer(ABC):
    @abstractmethod
    def update(self, temperature, humidity, pressure):
        ...


class WeatherStation:
    """The subject. It knows nothing about the concrete display classes."""

    def __init__(self, name):
        self.name = name
        self._observers = []
        self.temperature = None
        self.humidity = None
        self.pressure = None

    def subscribe(self, observer):
        if observer in self._observers:
            print(f"  {type(observer).__name__} is already subscribed")
            return False
        self._observers.append(observer)
        print(f"  + {type(observer).__name__} subscribed "
              f"({len(self._observers)} total)")
        return True

    def unsubscribe(self, observer):
        if observer not in self._observers:
            print(f"  {type(observer).__name__} was not subscribed")
            return False
        self._observers.remove(observer)
        print(f"  - {type(observer).__name__} unsubscribed "
              f"({len(self._observers)} left)")
        return True

    def notify(self):
        for obs in list(self._observers):
            obs.update(self.temperature, self.humidity, self.pressure)

    def set_measurements(self, temperature, humidity, pressure):
        print(f"\n[{self.name}] sensor reading: {temperature} C, "
              f"{humidity}% RH, {pressure} hPa")
        self.temperature = temperature
        self.humidity = humidity
        self.pressure = pressure
        self.notify()


class CurrentConditionsDisplay(Observer):
    def update(self, temperature, humidity, pressure):
        print(f"   [Current ] {temperature:.1f} C and {humidity:.0f}% humidity")


class StatisticsDisplay(Observer):
    def __init__(self):
        self.readings = []

    def update(self, temperature, humidity, pressure):
        self.readings.append(temperature)
        print(f"   [Stats   ] avg/min/max = "
              f"{sum(self.readings) / len(self.readings):.1f} / "
              f"{min(self.readings):.1f} / {max(self.readings):.1f} C "
              f"over {len(self.readings)} reading(s)")


class ForecastDisplay(Observer):
    def __init__(self):
        self.last_pressure = None

    def update(self, temperature, humidity, pressure):
        if self.last_pressure is None:
            trend = "no previous reading"
        elif pressure > self.last_pressure:
            trend = "improving weather on the way"
        elif pressure < self.last_pressure:
            trend = "cooler, rainy weather on the way"
        else:
            trend = "more of the same"
        self.last_pressure = pressure
        print(f"   [Forecast] {trend}")


class HeatAlertDisplay(Observer):
    THRESHOLD = 40.0

    def update(self, temperature, humidity, pressure):
        if temperature >= self.THRESHOLD:
            print(f"   [ALERT   ] heat warning, {temperature:.1f} C "
                  f"is above {self.THRESHOLD} C")


if __name__ == "__main__":
    station = WeatherStation("Pune Shivajinagar")

    current = CurrentConditionsDisplay()
    stats = StatisticsDisplay()
    forecast = ForecastDisplay()
    alert = HeatAlertDisplay()

    print("=== subscribing displays ===")
    for display in (current, stats, forecast, alert):
        station.subscribe(display)
    station.subscribe(current)                 # duplicate rejected

    station.set_measurements(31.4, 62, 1012)
    station.set_measurements(34.9, 55, 1009)

    print("\n=== one display unsubscribes, the rest keep working ===")
    station.unsubscribe(forecast)
    station.set_measurements(41.2, 38, 1005)

    print("\n=== resubscribing and removing an unknown observer ===")
    station.subscribe(forecast)
    station.unsubscribe(HeatAlertDisplay())    # never subscribed
    station.set_measurements(28.0, 71, 1011)

    print("\n=== the station is decoupled from display types ===")
    print("  station only stores:", [type(o).__name__ for o in station._observers])
    print("  all are Observer subclasses:",
          all(isinstance(o, Observer) for o in station._observers))
