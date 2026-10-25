
import unittest

from app.models import InventoryItem
from app.inventory import get_next_id


class TestInventory(unittest.TestCase):

    def test_empty_inventory_id(self):
        inventory = []

        result = get_next_id(inventory)

        self.assertEqual(result, 1)

    def test_next_inventory_id(self):
        inventory = [
            InventoryItem(
                id=1,
                name="Sol Ring",
                category="Magic Cards",
                quantity=2,
                location="Deck Box",
                notes="Commander staple"
            ),
            InventoryItem(
                id=2,
                name="Amazing Spider-Man #300",
                category="Comics",
                quantity=1,
                location="Comic Box",
                notes="Venom first full appearance"
            )
        ]

        result = get_next_id(inventory)

        self.assertEqual(result, 3)

    def test_id_after_gap(self):
        inventory = [
            InventoryItem(
                id=1,
                name="Sol Ring",
                category="Magic Cards",
                quantity=1,
                location="Binder",
                notes=""
            ),
            InventoryItem(
                id=5,
                name="Batman #1",
                category="Comics",
                quantity=1,
                location="Comic Box",
                notes=""
            )
        ]

        result = get_next_id(inventory)

        self.assertEqual(result, 6)


if __name__ == "__main__":
    unittest.main()
