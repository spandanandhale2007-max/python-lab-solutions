"""
Experiment 1 - Question 10: School Staff and Students

Scenario: A school management system differentiates Staff and Students while
sharing common features like name and address. Staff has subjects taught,
students have grades.

Rubrics covered:
  * inheritance from a base Person class
  * methods overridden in child classes
  * polymorphic display method
  * isinstance() / issubclass() demonstrated
"""


class Person:
    def __init__(self, name, age, address, phone):
        self.name = name
        self.age = age
        self.address = address
        self.phone = phone

    def role(self):
        return "Person"

    def display(self):                      # overridden by children
        print(f"{self.role():<8} | {self.name:<14} | age {self.age:<3} | "
              f"{self.address:<18} | {self.phone}")

    def __str__(self):
        return f"{self.role()}: {self.name}"


class Staff(Person):
    def __init__(self, name, age, address, phone, employee_id,
                 subjects, salary, department):
        super().__init__(name, age, address, phone)
        self.employee_id = employee_id
        self.subjects = list(subjects)
        self.salary = salary
        self.department = department

    def role(self):
        return "Staff"

    def teaching_load(self):
        return len(self.subjects)

    def display(self):                      # override
        super().display()
        print(f"         | emp-id {self.employee_id} | dept {self.department} | "
              f"subjects {', '.join(self.subjects)} | "
              f"load {self.teaching_load()} | Rs.{self.salary:,}/month")


class Student(Person):
    def __init__(self, name, age, address, phone, roll_no, standard, grades):
        super().__init__(name, age, address, phone)
        self.roll_no = roll_no
        self.standard = standard
        self.grades = dict(grades)          # subject -> marks

    def role(self):
        return "Student"

    def percentage(self):
        return sum(self.grades.values()) / len(self.grades) if self.grades else 0.0

    def result(self):
        return "PASS" if all(m >= 35 for m in self.grades.values()) else "FAIL"

    def display(self):                      # override
        super().display()
        marks = "  ".join(f"{s}:{m}" for s, m in self.grades.items())
        print(f"         | roll {self.roll_no} | std {self.standard} | {marks} | "
              f"{self.percentage():.2f}% | {self.result()}")


if __name__ == "__main__":
    people = [
        Staff("Mrs. Kulkarni", 41, "Kothrud, Pune", "9822001122",
              "EMP-17", ["Mathematics", "Statistics"], 68000, "Science"),
        Student("Spandan", 19, "Wakad, Pune", "9011223344",
                "CSE2301", "SY-CSE", {"Python": 88, "DSA": 92, "DBMS": 79}),
        Staff("Mr. Deshmukh", 35, "Hadapsar, Pune", "9765432100",
              "EMP-22", ["History"], 52000, "Humanities"),
        Student("Aman", 18, "Baner, Pune", "9834567812",
                "CSE2303", "SY-CSE", {"Python": 31, "DSA": 61, "DBMS": 48}),
    ]

    print("=== Polymorphic display(): one loop, four different outputs ===")
    for p in people:
        p.display()
        print("-" * 80)

    print("=== isinstance() filtering ===")
    staff = [p for p in people if isinstance(p, Staff)]
    students = [p for p in people if isinstance(p, Student)]
    print("Staff   :", [s.name for s in staff])
    print("Students:", [s.name for s in students])
    print(f"Monthly salary bill : Rs.{sum(s.salary for s in staff):,}")
    print(f"Class average       : "
          f"{sum(s.percentage() for s in students) / len(students):.2f}%")

    print("\n=== issubclass() checks ===")
    print("  Staff   subclass of Person :", issubclass(Staff, Person))
    print("  Student subclass of Person :", issubclass(Student, Person))
    print("  Student subclass of Staff  :", issubclass(Student, Staff))
    print("  every object is a Person   :", all(isinstance(p, Person) for p in people))
