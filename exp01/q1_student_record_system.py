"""
Experiment 1 - Question 1: Student Record System

Scenario: A college system maintains student records. Each student has a name,
roll number and three subject marks. Calculate the average and display
formatted details.

Rubrics covered:
  * __init__ initialises student data
  * instance methods for average and display
  * __str__ overridden for clean print
  * multiple students instantiated
"""


class Student:
    def __init__(self, name, roll_no, marks):
        if len(marks) != 3:
            raise ValueError("exactly three subject marks are required")
        self.name = name
        self.roll_no = roll_no
        self.marks = list(marks)

    def average(self):
        return sum(self.marks) / len(self.marks)

    def grade(self):
        avg = self.average()
        for cutoff, letter in ((90, "A+"), (80, "A"), (70, "B"), (60, "C"), (40, "D")):
            if avg >= cutoff:
                return letter
        return "F"

    def display(self):
        print(f"Roll No : {self.roll_no}")
        print(f"Name    : {self.name}")
        print(f"Marks   : {self.marks}")
        print(f"Average : {self.average():.2f}  (Grade {self.grade()})")
        print("-" * 40)

    def __str__(self):
        return (f"{self.roll_no} | {self.name:<12} | marks={self.marks} | "
                f"avg={self.average():.2f} | grade={self.grade()}")


if __name__ == "__main__":
    students = [
        Student("Spandan", "CSE2301", [88, 92, 79]),
        Student("Riya", "CSE2302", [95, 91, 98]),
        Student("Aman", "CSE2303", [55, 61, 48]),
    ]

    print("=== Detailed report (display method) ===")
    for s in students:
        s.display()

    print("=== One-line report (__str__ override) ===")
    for s in students:
        print(s)

    topper = max(students, key=Student.average)
    print(f"\nClass topper: {topper.name} with {topper.average():.2f}")
