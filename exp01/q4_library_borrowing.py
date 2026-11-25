"""
Experiment 1 - Question 4: Library Book Borrowing

Scenario: A library system where members borrow books. Each book has a title,
author and availability status. A member can borrow/return books and view the
borrowed list.

Rubrics covered:
  * two classes: Book and Member
  * composition (a Member holds Book objects)
  * book status tracked (borrowed/available)
  * borrowing and returning logic implemented
"""


class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.is_available = True
        self.borrowed_by = None

    def __str__(self):
        state = "available" if self.is_available else f"with {self.borrowed_by}"
        return f"{self.title:<28} by {self.author:<18} [{state}]"


class Member:
    MAX_BOOKS = 3

    def __init__(self, name, member_id):
        self.name = name
        self.member_id = member_id
        self.borrowed = []          # composition: Member has-a list of Book

    def borrow(self, book):
        if not book.is_available:
            print(f"DENIED  : '{book.title}' is already borrowed by {book.borrowed_by}")
            return False
        if len(self.borrowed) >= Member.MAX_BOOKS:
            print(f"DENIED  : {self.name} already holds {Member.MAX_BOOKS} books")
            return False
        book.is_available = False
        book.borrowed_by = self.name
        self.borrowed.append(book)
        print(f"ISSUED  : '{book.title}' -> {self.name}")
        return True

    def return_book(self, book):
        if book not in self.borrowed:
            print(f"DENIED  : {self.name} did not borrow '{book.title}'")
            return False
        self.borrowed.remove(book)
        book.is_available = True
        book.borrowed_by = None
        print(f"RETURNED: '{book.title}' <- {self.name}")
        return True

    def view_borrowed(self):
        print(f"\n{self.name} ({self.member_id}) has {len(self.borrowed)} book(s):")
        if not self.borrowed:
            print("   (none)")
        for b in self.borrowed:
            print("   -", b.title)

    def __str__(self):
        return f"<Member {self.name} books={len(self.borrowed)}>"


class Library:
    def __init__(self, name):
        self.name = name
        self.catalogue = []

    def add_book(self, book):
        self.catalogue.append(book)

    def show_catalogue(self):
        print(f"\n=== {self.name} catalogue ===")
        for b in self.catalogue:
            print("  ", b)


if __name__ == "__main__":
    lib = Library("MIT-WPU Central Library")
    b1 = Book("Python Crash Course", "Eric Matthes", "978-1593279288")
    b2 = Book("Clean Code", "Robert Martin", "978-0132350884")
    b3 = Book("Introduction to Algorithms", "Cormen", "978-0262033848")
    b4 = Book("Fluent Python", "Luciano Ramalho", "978-1492056355")
    for b in (b1, b2, b3, b4):
        lib.add_book(b)

    spandan = Member("Spandan", "M-101")
    riya = Member("Riya", "M-102")

    lib.show_catalogue()

    print("\n--- borrowing ---")
    spandan.borrow(b1)
    spandan.borrow(b2)
    riya.borrow(b1)          # already issued
    riya.borrow(b3)

    spandan.view_borrowed()
    riya.view_borrowed()

    print("\n--- returning ---")
    spandan.return_book(b1)
    spandan.return_book(b4)  # never borrowed
    riya.borrow(b1)          # now free

    lib.show_catalogue()
    spandan.view_borrowed()
    riya.view_borrowed()
