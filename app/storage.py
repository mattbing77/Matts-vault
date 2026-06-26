import json
from pathlib import Path

from app.models import InventoryItem


DATA_FILE = Path("data/inventory.json")


def load_inventory():
    if not DATA_FILE.exists():
        return []

    with open(DATA_FILE, "r") as file:
        data = json.load(file)

    return [InventoryItem(**item) for item in data]


def save_inventory(inventory):
    data = [item.__dict__ for item in inventory]

    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)