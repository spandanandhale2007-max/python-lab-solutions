"""
Experiment 1 - Question 5: Shape Hierarchy

Scenario: A geometry toolkit with a base class Shape and derived classes
Circle, Rectangle and Triangle with area calculations.

Rubrics covered:
  * common behaviour inherited from Shape
  * area() overridden (polymorphism)
  * base class reference used for derived objects
  * constructor chaining with super()
"""

import math
from abc import ABC, abstractmethod


class Shape(ABC):
    def __init__(self, name):
        self.name = name            # common state for every shape

    @abstractmethod
    def area(self):
        ...

    @abstractmethod
    def perimeter(self):
        ...

    def describe(self):             # common behaviour, inherited as-is
        return (f"{self.name:<10} area={self.area():8.2f}  "
                f"perimeter={self.perimeter():8.2f}")

    def __str__(self):
        return self.describe()


class Circle(Shape):
    def __init__(self, radius):
        super().__init__("Circle")          # constructor chaining
        self.radius = radius

    def area(self):
        return math.pi * self.radius ** 2

    def perimeter(self):
        return 2 * math.pi * self.radius


class Rectangle(Shape):
    def __init__(self, width, height):
        super().__init__("Rectangle")
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)


class Square(Rectangle):
    def __init__(self, side):
        super().__init__(side, side)        # two-level constructor chaining
        self.name = "Square"


class Triangle(Shape):
    def __init__(self, a, b, c):
        super().__init__("Triangle")
        if a + b <= c or b + c <= a or a + c <= b:
            raise ValueError("sides do not form a triangle")
        self.a, self.b, self.c = a, b, c

    def area(self):
        s = self.perimeter() / 2            # Heron's formula
        return math.sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))

    def perimeter(self):
        return self.a + self.b + self.c


if __name__ == "__main__":
    # a list of base-class references holding derived objects
    shapes = [Circle(5), Rectangle(8, 3), Square(4), Triangle(3, 4, 5)]

    print("=== polymorphic dispatch through Shape references ===")
    for s in shapes:
        print(s)

    print(f"\nTotal area of all shapes : {sum(s.area() for s in shapes):.2f}")
    biggest = max(shapes, key=lambda s: s.area())
    print(f"Largest shape            : {biggest.name} ({biggest.area():.2f})")

    print("\nType checks:")
    sq = shapes[2]
    print("  Square is a Rectangle :", isinstance(sq, Rectangle))
    print("  Square is a Shape     :", isinstance(sq, Shape))
    print("  Shape cannot be built :", end=" ")
    try:
        Shape("generic")
    except TypeError as e:
        print(type(e).__name__, "-", e)
