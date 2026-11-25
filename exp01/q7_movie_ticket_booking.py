"""
Experiment 1 - Question 7: Movie Ticket Booking

Scenario: A ticket booking system. Each theatre has a limited number of seats.
A customer can book a seat and the system tracks which seats are available.

Rubrics covered:
  * static (class) variables track seat availability and ticket count
  * double booking handled with a custom exception
  * modular design: Theater, Ticket, Customer classes
  * booking summary displayed
"""


class SeatUnavailableError(Exception):
    """Raised when a seat is already booked or does not exist."""


class Ticket:
    total_tickets_issued = 0          # static counter shared by all tickets

    def __init__(self, movie, seat, customer, price):
        Ticket.total_tickets_issued += 1
        self.ticket_id = f"TK{Ticket.total_tickets_issued:04d}"
        self.movie = movie
        self.seat = seat
        self.customer = customer
        self.price = price

    def __str__(self):
        return (f"{self.ticket_id} | {self.movie:<14} | seat {self.seat:<4} | "
                f"{self.customer:<10} | Rs.{self.price}")


class Customer:
    def __init__(self, name):
        self.name = name
        self.tickets = []

    def total_spent(self):
        return sum(t.price for t in self.tickets)

    def __str__(self):
        return f"{self.name} ({len(self.tickets)} ticket(s), Rs.{self.total_spent()})"


class Theater:
    seats_available = 0               # static view across all screens

    def __init__(self, name, movie, rows=3, cols=4, price=250):
        self.name = name
        self.movie = movie
        self.price = price
        self.seats = {f"{chr(65 + r)}{c + 1}": None
                      for r in range(rows) for c in range(cols)}
        Theater.seats_available += len(self.seats)

    def book(self, customer, seat):
        seat = seat.upper()
        if seat not in self.seats:
            raise SeatUnavailableError(f"seat {seat} does not exist in {self.name}")
        if self.seats[seat] is not None:
            raise SeatUnavailableError(
                f"seat {seat} is already booked by {self.seats[seat].customer}")
        ticket = Ticket(self.movie, seat, customer.name, self.price)
        self.seats[seat] = ticket
        customer.tickets.append(ticket)
        Theater.seats_available -= 1
        print(f"BOOKED  : {ticket}")
        return ticket

    def cancel(self, seat):
        seat = seat.upper()
        ticket = self.seats.get(seat)
        if ticket is None:
            raise SeatUnavailableError(f"seat {seat} is not booked")
        self.seats[seat] = None
        Theater.seats_available += 1
        print(f"CANCELED: {ticket}")

    def seat_map(self):
        print(f"\n--- {self.name}: {self.movie} ---")
        row = None
        for seat in sorted(self.seats):
            if seat[0] != row:
                row = seat[0]
                print(f"\n  Row {row}: ", end="")
            print("[XX]" if self.seats[seat] else f"[{seat}]", end=" ")
        free = sum(1 for t in self.seats.values() if t is None)
        print(f"\n  free {free}/{len(self.seats)}   (XX = booked)")

    def summary(self):
        sold = [t for t in self.seats.values() if t]
        print(f"\n=== Booking summary: {self.name} ===")
        for t in sold:
            print("  ", t)
        print(f"  Tickets sold : {len(sold)}")
        print(f"  Revenue      : Rs.{sum(t.price for t in sold)}")


if __name__ == "__main__":
    pvr = Theater("PVR Screen 2", "Dune Part Two", rows=3, cols=4, price=280)
    spandan, riya = Customer("Spandan"), Customer("Riya")

    pvr.seat_map()

    print("\n--- bookings ---")
    pvr.book(spandan, "A1")
    pvr.book(spandan, "A2")
    pvr.book(riya, "B3")

    print("\n--- double booking and a bad seat ---")
    for cust, seat in ((riya, "A1"), (riya, "Z9")):
        try:
            pvr.book(cust, seat)
        except SeatUnavailableError as e:
            print("REJECTED:", e)

    print("\n--- cancellation then rebooking ---")
    pvr.cancel("A2")
    pvr.book(riya, "A2")

    pvr.seat_map()
    pvr.summary()
    print(f"\nStatic counters -> tickets issued: {Ticket.total_tickets_issued}, "
          f"seats free across all screens: {Theater.seats_available}")
    print("Customers:", spandan, "|", riya)
