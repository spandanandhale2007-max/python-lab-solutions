"""
Experiment 2 - Question 3: Animal Zoo with Polymorphism

Scenario: A zoo simulator. Each animal has a speak() method. Lion, Monkey and
Snake inherit from a base Animal class and override the behaviour.

Rubrics covered:
  * class hierarchy implemented
  * polymorphism demonstrated through speak()
  * a list of mixed animal objects is used
  * a loop invokes the behaviour dynamically
"""


class Animal:
    def __init__(self, name, age, diet="omnivore"):
        self.name = name
        self.age = age
        self.diet = diet

    def speak(self):
        return "..."

    def move(self):
        return "moves around"

    def enclosure(self):
        return "General Enclosure"

    def info(self):
        return (f"{type(self).__name__:<8} {self.name:<8} age {self.age:<3} "
                f"{self.diet:<10} | says {self.speak():<22} | {self.move():<18} "
                f"| {self.enclosure()}")


class Lion(Animal):
    def __init__(self, name, age, mane_size="large"):
        super().__init__(name, age, diet="carnivore")
        self.mane_size = mane_size

    def speak(self):
        return "ROAAAR!"

    def move(self):
        return "prowls on 4 legs"

    def enclosure(self):
        return "Big Cat Safari"


class Monkey(Animal):
    def __init__(self, name, age, troop_size=5):
        super().__init__(name, age, diet="frugivore")
        self.troop_size = troop_size

    def speak(self):
        return "Ooh ooh aah aah!"

    def move(self):
        return "swings on branches"

    def enclosure(self):
        return "Primate Canopy"


class Snake(Animal):
    def __init__(self, name, age, venomous=True):
        super().__init__(name, age, diet="carnivore")
        self.venomous = venomous

    def speak(self):
        return "Ssssssss..."

    def move(self):
        return "slithers"

    def enclosure(self):
        return "Reptile House" + (" (venomous)" if self.venomous else "")


class Parrot(Animal):
    def __init__(self, name, age, phrase="Hello!"):
        super().__init__(name, age, diet="granivore")
        self.phrase = phrase

    def speak(self):
        return f"{self.phrase} {self.phrase}"

    def move(self):
        return "flies"

    def enclosure(self):
        return "Aviary"


if __name__ == "__main__":
    # a single list holding objects of different concrete types
    zoo = [
        Lion("Simba", 7),
        Monkey("Rafiki", 4, troop_size=11),
        Snake("Kaa", 3, venomous=False),
        Parrot("Iago", 2, phrase="Polly wants a samosa!"),
        Animal("Mystery", 1),
    ]

    print("=== Morning roll call (one loop, many behaviours) ===")
    for animal in zoo:
        print(animal.info())

    print("\n=== Feeding round: dispatch decided at runtime ===")
    for animal in zoo:
        print(f"  {animal.name:<8} ({animal.diet:<10}) -> {animal.speak()}")

    print("\n=== Grouping by enclosure ===")
    groups = {}
    for animal in zoo:
        groups.setdefault(animal.enclosure(), []).append(animal.name)
    for place, names in groups.items():
        print(f"  {place:<24} {', '.join(names)}")

    print("\n=== Same method name, different code objects ===")
    for cls in (Lion, Monkey, Snake, Parrot):
        print(f"  {cls.__name__:<8} speak defined in -> "
              f"{cls.speak.__qualname__}  (overrides Animal.speak: "
              f"{cls.speak is not Animal.speak})")
