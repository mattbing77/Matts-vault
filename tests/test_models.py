import unittest

from app.models import InventoryItem, MagicCard, ComicBook


class TestModels(unittest.TestCase):

    def test_magic_card_creation(self):
        card = MagicCard(
            id=1,
            name="Sol Ring",
            category="Magic Cards",
            quantity=2,
            location="Binder",
            notes="Commander staple",
            set_code="CMM",
            collector_number="396",
            finish="Nonfoil",
        )

        self.assertIsInstance(card, InventoryItem)
        self.assertEqual(card.name, "Sol Ring")
        self.assertEqual(card.set_code, "CMM")
        self.assertEqual(card.quantity, 2)

    def test_comic_book_creation(self):
        comic = ComicBook(
            id=2,
            name="Amazing Spider-Man #300",
            category="Comics",
            quantity=1,
            location="Comic Box",
            notes="First full Venom appearance",
            series="Amazing Spider-Man",
            issue_number="300",
            publisher="Marvel",
            publication_year=1988,
        )

        self.assertIsInstance(comic, InventoryItem)
        self.assertEqual(comic.issue_number, "300")
        self.assertEqual(comic.publisher, "Marvel")
        self.assertEqual(comic.publication_year, 1988)

    def test_magic_card_defaults(self):
        card = MagicCard(
            id=3,
            name="Lightning Bolt",
            category="Magic Cards",
            quantity=4,
            location="Binder",
            notes="",
        )

        self.assertEqual(card.finish, "Nonfoil")
        self.assertEqual(card.deck_assignment, "")
        self.assertEqual(card.condition, "")


if __name__ == "__main__":
    unittest.main()