from app.models import InventoryItem
from app.storage import load_inventory, save_inventory


def main():
    # Load existing inventory
    inventory = load_inventory()

    # Create a new inventory item
    new_item = InventoryItem(
        id=1,
        name="Sol Ring",
        category="Magic Card",
        quantity=1,
        location="Commander Binder",
        notes="First test item"
    )

    # Add it to inventory
    inventory.append(new_item)

    # Save inventory
    save_inventory(inventory)

    print("Item saved successfully!")

    # Reload inventory to verify it worked
    inventory = load_inventory()

    print("\nCurrent Inventory:")
    for item in inventory:
        print(item)


if __name__ == "__main__":
    main()