
from app.models import InventoryItem
from app.storage import load_inventory, save_inventory


# ==========================================
# HELPER FUNCTIONS
# ==========================================

def pause():
    input("\nPress Enter to continue...")


def display_item(item):
    print(f"ID: {item.id}")
    print(f"Name: {item.name}")
    print(f"Category: {item.category}")
    print(f"Quantity: {item.quantity}")
    print(f"Location: {item.location}")
    print(f"Notes: {item.notes}")
    print("-----------------------")


def choose_category(allow_skip=False):
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

    while True:
        choice = input("Choose a category: ").strip()

        if allow_skip and choice == "":
            return None

        if choice in categories:
            return categories[choice]

        print(
            "Error: Invalid category. "
            "Please enter a number between 1 and 6."
        )


def get_next_id(inventory):
    if not inventory:
        return 1

    highest_id = max(item.id for item in inventory)
    return highest_id + 1


def get_valid_quantity():
    while True:
        user_input = input("Quantity: ").strip()

        if not user_input.isdigit():
            print(
                "Error: Invalid quantity. "
                "Please enter a positive whole number."
            )
            continue

        quantity = int(user_input)

        if quantity <= 0:
            print("Error: Quantity must be greater than zero.")
            continue

        return quantity


def get_valid_name():
    while True:
        name = input("Item name: ").strip()

        if name:
            return name

        print(
            "Error: Item name cannot be empty. "
            "Please enter an item name."
        )


def find_item_by_id(inventory):
    while True:
        user_input = input("Enter Item ID (0 to cancel): ").strip()

        if not user_input.isdigit():
            print(
                "Error: Invalid ID. "
                "Please enter a numeric item ID."
            )
            continue

        item_id = int(user_input)

        if item_id == 0:
            return None

        for item in inventory:
            if item.id == item_id:
                return item

        print(
            "Error: No item found with that ID. "
            "Please try again or enter 0 to cancel."
        )


# ==========================================
# VIEW INVENTORY
# ==========================================

def view_inventory():
    inventory = load_inventory()

    print()
    print("=======================")
    print("      Inventory")
    print("=======================")

    if not inventory:
        print("No items found.")
        pause()
        return

    for item in inventory:
        display_item(item)

    pause()


# ==========================================
# ADD ITEM
# ==========================================

def add_item():
    inventory = load_inventory()

    print()
    print("=======================")
    print("      Add Item")
    print("=======================")

    name = get_valid_name()
    category = choose_category()
    if category is None:
        raise ValueError("Category is required when adding an item.")
    quantity = get_valid_quantity()
    location = input("Location: ").strip()
    notes = input("Notes: ").strip()

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
    print(f"Assigned Item ID: {new_item.id}")

    pause()


# ==========================================
# SEARCH INVENTORY
# ==========================================

def search_inventory():
    inventory = load_inventory()

    print()
    print("=======================")
    print("   Search Inventory")
    print("=======================")

    if not inventory:
        print("No items found.")
        pause()
        return

    while True:
        search_term = input(
            "Search by name, category, or location: "
        ).strip().lower()

        if search_term:
            break

        print(
            "Error: Search cannot be empty. "
            "Please enter a search term."
        )

    results = []

    for item in inventory:
        if (
            search_term in item.name.lower()
            or search_term in item.category.lower()
            or search_term in item.location.lower()
        ):
            results.append(item)

    print()

    if not results:
        print("No matching items found.")
    else:
        print(f"Found {len(results)} matching item(s).")
        print("-----------------------")

        for item in results:
            display_item(item)

    pause()


# ==========================================
# UPDATE ITEM
# ==========================================

def update_item():
    inventory = load_inventory()

    print()
    print("=======================")
    print("      Update Item")
    print("=======================")

    if not inventory:
        print("No items found.")
        pause()
        return

    item = find_item_by_id(inventory)

    if item is None:
        print("Update cancelled.")
        pause()
        return

    print()
    print("Current Item:")
    print("-----------------------")
    display_item(item)

    print()
    print("Press Enter to keep the current value.")

    # Update name
    new_name = input("New Name: ").strip()

    if new_name:
        item.name = new_name

    # Update category
    print()
    print(f"Current Category: {item.category}")
    print("Press Enter to keep the current category.")

    new_category = choose_category(allow_skip=True)

    if new_category is not None:
        item.category = new_category

    # Update quantity
    while True:
        new_quantity = input("New Quantity: ").strip()

        if not new_quantity:
            break

        if not new_quantity.isdigit():
            print(
                "Error: Invalid quantity. "
                "Please enter a positive whole number."
            )
            continue

        quantity = int(new_quantity)

        if quantity <= 0:
            print("Error: Quantity must be greater than zero.")
            continue

        item.quantity = quantity
        break

    # Update location
    new_location = input("New Location: ").strip()

    if new_location:
        item.location = new_location

    # Update notes
    new_notes = input("New Notes: ").strip()

    if new_notes:
        item.notes = new_notes

    save_inventory(inventory)

    print()
    print("Item updated successfully!")

    pause()


# ==========================================
# DELETE ITEM
# ==========================================

def delete_item():
    inventory = load_inventory()

    print()
    print("=======================")
    print("      Delete Item")
    print("=======================")

    if not inventory:
        print("No items found.")
        pause()
        return

    item = find_item_by_id(inventory)

    if item is None:
        print("Deletion cancelled.")
        pause()
        return

    print()
    print("Item selected for deletion:")
    print("-----------------------")
    display_item(item)

    while True:
        confirmation = input(
            "Are you sure you want to delete this item? (y/n): "
        ).strip().lower()

        if confirmation == "y":
            inventory.remove(item)
            save_inventory(inventory)

            print()
            print("Item deleted successfully!")
            break

        elif confirmation == "n":
            print("Deletion cancelled.")
            break

        else:
            print(
                "Error: Invalid answer. "
                "Please enter 'y' for yes or 'n' for no."
            )

    pause()
