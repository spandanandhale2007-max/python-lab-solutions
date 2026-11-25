"""
Experiment 2 - Question 1: Game Character with Equipment

Scenario: A simple RPG system where each Character is equipped with a Weapon
and Armor. Equipment affects the character's total attack/defence power.

Rubrics covered:
  * composition: Character has-a Weapon and an Armor
  * modular design of each class
  * aggregated calculation of stats
  * full character summary printed
"""


class Weapon:
    def __init__(self, name, attack, crit_chance=0.1):
        self.name = name
        self.attack = attack
        self.crit_chance = crit_chance

    def __str__(self):
        return f"{self.name} (+{self.attack} atk, {self.crit_chance:.0%} crit)"


class Armor:
    def __init__(self, name, defence, weight):
        self.name = name
        self.defence = defence
        self.weight = weight

    def __str__(self):
        return f"{self.name} (+{self.defence} def, {self.weight} kg)"


class Character:
    """Composition: the character owns a Weapon object and an Armor object."""

    def __init__(self, name, cls_name, base_attack, base_defence,
                 weapon=None, armor=None):
        self.name = name
        self.cls_name = cls_name
        self.base_attack = base_attack
        self.base_defence = base_defence
        self.weapon = weapon          # has-a
        self.armor = armor            # has-a
        self.hp = 100

    def equip_weapon(self, weapon):
        self.weapon = weapon
        print(f"{self.name} equips {weapon.name}")

    def equip_armor(self, armor):
        self.armor = armor
        print(f"{self.name} equips {armor.name}")

    # --- aggregated stats ---
    def total_attack(self):
        return self.base_attack + (self.weapon.attack if self.weapon else 0)

    def total_defence(self):
        return self.base_defence + (self.armor.defence if self.armor else 0)

    def speed(self):
        return max(1, 20 - (self.armor.weight if self.armor else 0))

    def power_score(self):
        return self.total_attack() * 2 + self.total_defence() + self.speed()

    def attack_target(self, other):
        damage = max(1, self.total_attack() - other.total_defence() // 2)
        other.hp -= damage
        print(f"{self.name} hits {other.name} for {damage} "
              f"({other.name} hp -> {max(0, other.hp)})")

    def summary(self):
        print(f"\n===== {self.name} the {self.cls_name} =====")
        print(f"  Weapon       : {self.weapon or 'bare hands'}")
        print(f"  Armor        : {self.armor or 'cloth rags'}")
        print(f"  Attack       : {self.base_attack} base -> {self.total_attack()}")
        print(f"  Defence      : {self.base_defence} base -> {self.total_defence()}")
        print(f"  Speed        : {self.speed()}")
        print(f"  HP           : {self.hp}")
        print(f"  Power score  : {self.power_score()}")


if __name__ == "__main__":
    excalibur = Weapon("Excalibur", 35, 0.25)
    dagger = Weapon("Rusty Dagger", 8, 0.05)
    plate = Armor("Steel Plate", 30, 14)
    leather = Armor("Leather Vest", 10, 3)

    knight = Character("Arthur", "Knight", 20, 15, excalibur, plate)
    thief = Character("Mira", "Thief", 14, 6, dagger, leather)

    knight.summary()
    thief.summary()

    print("\n--- swapping equipment changes aggregated stats ---")
    thief.equip_weapon(excalibur)
    thief.summary()

    print("\n--- combat round ---")
    knight.equip_weapon(dagger)
    knight.attack_target(thief)
    thief.attack_target(knight)

    print("\n--- final power ranking ---")
    for c in sorted([knight, thief], key=Character.power_score, reverse=True):
        print(f"  {c.name:<8} power={c.power_score()}  hp={c.hp}")
