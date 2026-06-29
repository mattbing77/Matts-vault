from app.storage import load_inventory
from app.models import InventoryItem
from app.storage import load_inventory, save_inventory

def view_inventory():
    inventory = load_inventory()

    print()
    print("=======================")
    print("      Inventory")
    print("=======================")

    if not inventory:
        print("No items found.")
        print()
        input("Press Enter to continue...")
        return

    for item in inventory:
        print(f"ID: {item.id}")
        print(f"Name: {item.name}")
        print(f"Category: {item.category}")
        print(f"Quantity: {item.quantity}")
        print(f"Location: {item.location}")
        print(f"Notes: {item.notes}")
        print("-----------------------")

    input("Press Enter to continue...")

def choose_category():
    categories = {
        "1": "Magic Cards",
        "2": "Comics",
        "3": "Gym",
        "4": "Groceries",
        "5": "Electronics",
        "6": "Other",
    }

    print()
    print("Select Category")
    print("-----------------------")
    for number, category in categories.items():
        print(f"{number}. {category}")

    choice = input("Choose a category: ")

    return categories.get(choice, "Other")

def get_next_id(inventory):
    if not inventory:
        return 1

    highest_id = max(item.id for item in inventory)
    return highest_id + 1

def get_valid_quantity():
    while True:
        user_input = input("Quantity: ").strip()

        if not user_input.isdigit():
            print("Error: Invalid quantity. Please enter a whole number.")
            continue

        quantity = int(user_input)

        if quantity <= 0:
            print("Error: Quantity must be greater than zero.")
            continue

        return quantity


def add_item():
    inventory = load_inventory()

    print()
    print("=======================")
    print("      Add Item")
    print("=======================")

    while True:
        name = input("Item name: ").strip()

        if name:
            break
        
        print("Error: Item name cannot be empty. Please enter an item name.")
    category = choose_category()
    quantity = get_valid_quantity()    
    location = input("Location: ")
    notes = input("Notes: ")

    new_item = InventoryItem(
        id=get_next_id(inventory),
        name=name,
        category=category,
        quantity=quantity,
        location=location,
        notes=notes,
    )

    inventory.append(new_item)
    save_inventory(inventory)

    print()
    print("Item added successfully!")
    input("Press Enter to continue...")