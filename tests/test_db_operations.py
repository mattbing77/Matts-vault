import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.database import Base
from app.db_models import InventoryRecord, MagicCardRecord, ComicBookRecord, ItemImageRecord
from app.db_operations import (create_item, get_all_items, get_item_by_id,
    update_item,
    delete_item,
    create_magic_card,
    create_comic_book)


class TestDatabaseOperations(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine(
            "sqlite://",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )

        Base.metadata.create_all(self.engine)
        self.session = Session(self.engine)

    def tearDown(self):
        self.session.close()
        self.engine.dispose()

    def test_create_item(self):
        item = create_item(
            self.session,
            name="Sol Ring",
            category="Magic Cards",
            quantity=2,
            location="Binder",
            notes="Commander staple",
        )

        self.assertIsNotNone(item.id)
        self.assertEqual(item.name, "Sol Ring")
        self.assertEqual(item.quantity, 2)

        saved_item = self.session.get(InventoryRecord, item.id)

        self.assertIsNotNone(saved_item)

        if saved_item is None:
            self.fail("Inventory item was not saved to the database.")

        self.assertEqual(saved_item.name, "Sol Ring")

    def test_get_all_items(self):
        create_item(
            self.session,
            name="Sol Ring",
            category="Magic Cards",
        )

        create_item(
            self.session,
            name="Amazing Spider-Man #300",
            category="Comics",
        )

        items = get_all_items(self.session)

        self.assertEqual(len(items), 2)
        self.assertEqual(items[0].name, "Sol Ring")
        self.assertEqual(items[1].name, "Amazing Spider-Man #300")

    def test_reject_empty_name(self):
        with self.assertRaises(ValueError):
            create_item(
                self.session,
                name="  ",
                category="Magic Cards",
            )

    def test_reject_negative_quantity(self):
        with self.assertRaises(ValueError):
            create_item(
                self.session,
                name="Sol Ring",
                category="Magic Cards",
                quantity=-1,
            )

    def test_get_item_by_id(self):
            item = create_item(
            self.session,
            name="Sol Ring",
            category="Magic Cards",
        )

            found = get_item_by_id(self.session, item.id)

            self.assertIsNotNone(found)
            assert found is not None
            self.assertEqual(found.name, "Sol Ring")

    def test_get_missing_item(self):
        result = get_item_by_id(self.session, 999)
        self.assertIsNone(result)

    def test_update_item(self):
        item = create_item(
            self.session,
            name="Sol Ring",
            category="Magic Cards",
            quantity=1,
        )

        updated = update_item(
            self.session,
            item.id,
            quantity=4,
            location="Commander Binder",
        )

        self.assertIsNotNone(updated)
        assert updated is not None
        self.assertEqual(updated.quantity, 4)
        self.assertEqual(updated.location, "Commander Binder")
        self.assertEqual(updated.name, "Sol Ring")

    def test_delete_item(self):
        item = create_item(
            self.session,
            name="Sol Ring",
            category="Magic Cards",
        )

        result = delete_item(self.session, item.id)

        self.assertTrue(result)
        self.assertIsNone(get_item_by_id(self.session, item.id))

    def test_delete_missing_item(self):
        result = delete_item(self.session, 999)
        self.assertFalse(result)
    def test_create_magic_card_with_details(self):
        item = create_item(
            self.session,
            name="Sol Ring",
            category="Magic Cards",
            quantity=2,
            location="Binder",
        )

        item.magic_card = MagicCardRecord(
            set_code="CMM",
            collector_number="396",
            finish="Nonfoil",
            condition="Near Mint",
            deck_assignment="The Scarab God",
        )

        self.session.commit()
        self.session.expire_all()

        saved = self.session.get(InventoryRecord, item.id)

        self.assertIsNotNone(saved)
        if saved is None:
            self.fail("Magic card was not saved.")

        self.assertIsNotNone(saved.magic_card)
        if saved.magic_card is None:
            self.fail("Magic card details were not saved.")

        self.assertEqual(saved.magic_card.set_code, "CMM")
        self.assertEqual(
            saved.magic_card.deck_assignment,
            "The Scarab God",
        )

    def test_create_comic_with_details(self):
        item = create_item(
            self.session,
            name="Amazing Spider-Man #300",
            category="Comics",
            quantity=1,
            location="Comic Box",
        )

        item.comic_book = ComicBookRecord(
            series="Amazing Spider-Man",
            issue_number="300",
            publisher="Marvel",
            publication_year=1988,
            variant="",
            grade="Very Fine",
        )

        self.session.commit()
        self.session.expire_all()

        saved = self.session.get(InventoryRecord, item.id)

        self.assertIsNotNone(saved)
        if saved is None:
            self.fail("Comic book was not saved.")

        self.assertIsNotNone(saved.comic_book)
        if saved.comic_book is None:
            self.fail("Comic book details were not saved.")

        self.assertEqual(saved.comic_book.issue_number, "300")
        self.assertEqual(saved.comic_book.publication_year, 1988)
    def test_create_magic_card_function(self):
        item = create_magic_card(
            self.session,
            name="Sol Ring",
            quantity=2,
            set_code="CMM",
            collector_number="396",
            finish="Nonfoil",
            condition="Near Mint",
        )

        self.assertEqual(item.category, "Magic Cards")

        self.session.expire_all()
        saved = self.session.get(InventoryRecord, item.id)

        self.assertIsNotNone(saved)
        if saved is None:
            self.fail("Magic card inventory record was not saved.")

        self.assertIsNotNone(saved.magic_card)
        if saved.magic_card is None:
            self.fail("Magic card details were not saved.")

        self.assertEqual(saved.magic_card.set_code, "CMM")
        self.assertEqual(saved.magic_card.condition, "Near Mint")

    def test_create_comic_book_function(self):
        item = create_comic_book(
            self.session,
            name="Amazing Spider-Man #300",
            series="Amazing Spider-Man",
            issue_number="300",
            publisher="Marvel",
            publication_year=1988,
            grade="Very Fine",
        )

        self.assertEqual(item.category, "Comics")

        self.session.expire_all()
        saved = self.session.get(InventoryRecord, item.id)

        self.assertIsNotNone(saved)
        if saved is None:
            self.fail("Comic inventory record was not saved.")

        self.assertIsNotNone(saved.comic_book)
        if saved.comic_book is None:
            self.fail("Comic details were not saved.")

        self.assertEqual(saved.comic_book.issue_number, "300")
        self.assertEqual(saved.comic_book.publication_year, 1988)
    def test_add_image_to_comic(self):
        item = create_comic_book(
            self.session,
            name="Amazing Spider-Man #300",
            series="Amazing Spider-Man",
            issue_number="300",
        )

        item.images.append(
            ItemImageRecord(
                storage_key="comics/300/front.jpg",
                is_primary=True,
            )
        )

        self.session.commit()
        self.session.expire_all()

        saved = self.session.get(InventoryRecord, item.id)

        self.assertIsNotNone(saved)
        if saved is None:
            self.fail("Comic inventory record was not saved.")

        self.assertEqual(len(saved.images), 1)
        self.assertEqual(
            saved.images[0].storage_key,
            "comics/300/front.jpg",
        )
        self.assertTrue(saved.images[0].is_primary)
if __name__ == "__main__":
    unittest.main()