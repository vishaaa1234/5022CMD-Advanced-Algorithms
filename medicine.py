"""medicine.py - Entity class for one pharmacy product."""


class Medicine:
    """A single pharmacy product.

    medicine_id : int   - unique key used by the hash table
    name        : str   - product name (text)
    price       : float - price in RM (decimal value)
    quantity    : int   - stock in whole units
    category    : str   - e.g. "Pain relief", "Vitamin"
    """

    def __init__(self, medicine_id, name, price, quantity, category="General"):
        if price < 0 or quantity < 0:
            raise ValueError("Price and quantity cannot be negative.")
        self.medicine_id = medicine_id
        self.name = name
        self.price = price
        self.quantity = quantity
        self.category = category

    def display_info(self):
        print(f"Medicine ID: {self.medicine_id}")
        print(f"Name: {self.name}")
        print(f"Category: {self.category}")
        print(f"Price: RM{self.price:.2f}")
        print(f"Quantity: {self.quantity}")

    def __str__(self):
        return (f"ID: {self.medicine_id} | Name: {self.name} | "
                f"Price: RM{self.price:.2f} | Stock: {self.quantity}")
