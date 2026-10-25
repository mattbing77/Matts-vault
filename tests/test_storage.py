
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from app.models import InventoryItem
from app.storage import load_inventory, save_inventory


class TestStorage(unittest.TestCase):

    def test_save_and_load_inventory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            test_file = Path(temp_dir) / "inventory.json"

            with patch("app.storage.DATA_FILE", test_file):
                inventory = [
                    InventoryItem(
                        id=1,
                        name="Sol Ring",
                        category="Magic Cards",
                        quantity=3,
                        location="Deck Box",
                        notes="Commander staple"
                    )
                ]

                save_inventory(inventory)
                loaded_inventory = load_inventory()

                self.assertEqual(len(loaded_inventory), 1)
                self.assertEqual(loaded_inventory[0], inventory[0])

    def test_missing_inventory_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            test_file = Path(temp_dir) / "missing.json"

            with patch("app.storage.DATA_FILE", test_file):
                loaded_inventory = load_inventory()

                self.assertEqual(loaded_inventory, [])

    def test_empty_inventory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            test_file = Path(temp_dir) / "inventory.json"

            with patch("app.storage.DATA_FILE", test_file):
                save_inventory([])
                loaded_inventory = load_inventory()

                self.assertEqual(loaded_inventory, [])


if __name__ == "__main__":
    unittest.main()
