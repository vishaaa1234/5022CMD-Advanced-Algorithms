"""
inventory.py - Command-line Pharmacy Inventory System.

PharmacyInventory keeps every Medicine in a HashTable and, in parallel, in a
plain list (one-dimensional array) so each search can be timed on both.
"""

import time

from hashtable import HashTable, DELETED
from medicine import Medicine


def linear_search(array, medicine_id):
    """Sequential search of a one-dimensional array: O(n)."""
    for medicine in array:
        if medicine.medicine_id == medicine_id:
            return medicine
    return None


class PharmacyInventory:
    def __init__(self, table_size=7):
        self.table = HashTable(table_size)
        self.array = []

    def insert(self, medicine):
        """Return the slot index, or None if the ID already exists."""
        if self.table.search(medicine.medicine_id) is not None:
            return None
        slot = self.table.insert(medicine.medicine_id, medicine)
        self.array.append(medicine)
        return slot

    def search(self, medicine_id):
        return self.table.search(medicine_id)

    def timed_search(self, medicine_id):
        """Return (medicine, hash_time_ns, array_time_ns)."""
        start = time.perf_counter_ns()
        found = self.table.search(medicine_id)
        hash_ns = time.perf_counter_ns() - start

        start = time.perf_counter_ns()
        linear_search(self.array, medicine_id)
        array_ns = time.perf_counter_ns() - start
        return found, hash_ns, array_ns

    def delete(self, medicine_id):
        medicine = self.table.search(medicine_id)
        if medicine is None:
            return False
        self.table.delete(medicine_id)
        self.array.remove(medicine)
        return True

    def load_predefined(self):
        records = [
            Medicine(102, "Paracetamol", 5.50, 100, "Pain relief"),
            Medicine(109, "Ibuprofen", 8.90, 50, "Pain relief"),
            Medicine(116, "Cetirizine", 6.50, 75, "Allergy"),
            Medicine(103, "Vitamin C", 12.00, 40, "Vitamin"),
            Medicine(110, "Antacid", 4.50, 60, "Digestive"),
        ]
        for medicine in records:
            self.insert(medicine)


# ------------------------------------------------------------ input helpers
def read_int(prompt, minimum=None):
    while True:
        try:
            value = int(input(prompt))
            if minimum is not None and value < minimum:
                print(f"Value must be at least {minimum}.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a whole number.")


def read_float(prompt, minimum=None):
    while True:
        try:
            value = float(input(prompt))
            if minimum is not None and value < minimum:
                print(f"Value must be at least {minimum}.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a number.")


def read_text(prompt):
    while True:
        text = input(prompt).strip()
        if text:
            return text
        print("This field cannot be empty.")


# ------------------------------------------------------------ menu actions
def insert_medicine(inventory):
    print("\n--- INSERT MEDICINE ---")
    medicine_id = read_int("Enter Medicine ID: ", 0)
    if inventory.search(medicine_id) is not None:
        print("Medicine ID already exists.")
        return
    name = read_text("Enter Medicine Name: ")
    price = read_float("Enter Medicine Price (RM): ", 0)
    quantity = read_int("Enter Quantity: ", 0)
    category = input("Enter Category (optional): ").strip() or "General"

    slot = inventory.insert(Medicine(medicine_id, name, price, quantity, category))
    print(f"Medicine inserted successfully into slot [{slot}]")


def search_medicine(inventory):
    print("\n--- SEARCH MEDICINE ---")
    medicine_id = read_int("Enter Medicine ID: ", 0)
    medicine, hash_ns, array_ns = inventory.timed_search(medicine_id)
    if medicine is None:
        print("Medicine not found.")
        return
    print("\nMedicine Found!")
    print(medicine)
    print(f"Search completed in {hash_ns / 1e9:.6f} seconds ({hash_ns:,} ns) (Hash Table)")
    print(f"Search completed in {array_ns / 1e9:.6f} seconds ({array_ns:,} ns) (Array - same record)")


def edit_medicine(inventory):
    print("\n--- EDIT MEDICINE ---")
    medicine_id = read_int("Enter Medicine ID to edit: ", 0)
    medicine = inventory.search(medicine_id)
    if medicine is None:
        print("Medicine not found.")
        return
    print("\nCurrent Medicine Details:")
    medicine.display_info()
    print("\nPress Enter to keep the current value.")
    name = input("Enter New Name: ").strip()
    price = input("Enter New Price (RM): ").strip()
    quantity = input("Enter New Quantity: ").strip()
    try:
        if name:
            medicine.name = name
        if price:
            medicine.price = float(price)
        if quantity:
            medicine.quantity = int(quantity)
        print("\nMedicine updated successfully!")
    except ValueError:
        print("Invalid number entered. Remaining changes were not applied.")


def delete_medicine(inventory):
    print("\n--- DELETE MEDICINE ---")
    medicine_id = read_int("Enter Medicine ID to delete: ", 0)
    if inventory.delete(medicine_id):
        print("Medicine deleted successfully!")
    else:
        print("Medicine not found.")


def display_medicines(inventory):
    table = inventory.table
    print(f"\n--- PHARMACY INVENTORY (size {table.size}, "
          f"load factor {table.load_factor:.2f}) ---")
    for index, slot in enumerate(table.table):
        if slot is None:
            print(f"Slot {index}: Empty")
        elif slot is DELETED:
            print(f"Slot {index}: Deleted")
        else:
            print(f"Slot {index}: {slot[1]}")


def main():
    inventory = PharmacyInventory(table_size=7)
    inventory.load_predefined()

    actions = {
        "1": insert_medicine,
        "2": search_medicine,
        "3": display_medicines,
        "4": edit_medicine,
        "5": delete_medicine,
    }
    while True:
        print("\n" + "=" * 32)
        print("     PHARMACY INVENTORY SYSTEM")
        print("=" * 32)
        print("1. Insert Medicine")
        print("2. Search Medicine")
        print("3. Display All Medicines")
        print("4. Edit Medicine")
        print("5. Delete Medicine")
        print("6. Exit")
        choice = input("\nEnter your choice: ").strip()

        if choice == "6":
            print("Exiting Pharmacy Inventory System...")
            break
        action = actions.get(choice)
        if action:
            action(inventory)
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
