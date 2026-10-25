import unittest

from sqlalchemy import create_engine, inspect
from sqlalchemy.pool import StaticPool

from app.database import Base
from app.db_models import InventoryRecord


class TestDatabase(unittest.TestCase):

    def test_inventory_table_creation(self):
        test_engine = create_engine(
            "sqlite://",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )

        try:
            Base.metadata.create_all(test_engine)

            tables = inspect(test_engine).get_table_names()

            self.assertIn("inventory_items", tables)
        finally:
            test_engine.dispose()

    def test_inventory_record_creation(self):
        record = InventoryRecord(
            name="Sol Ring",
            category="Magic Cards",
            quantity=2,
            location="Binder",
            notes="Commander staple",
        )

        self.assertEqual(record.name, "Sol Ring")
        self.assertEqual(record.quantity, 2)