from dataclasses import dataclass


@dataclass
class InventoryItem:
    id: int
    name: str
    category: str
    quantity: int
    location: str
    notes: str


@dataclass
class MagicCard(InventoryItem):
    set_code: str = ""
    collector_number: str = ""
    finish: str = "Nonfoil"
    condition: str = ""
    deck_assignment: str = ""


@dataclass
class ComicBook(InventoryItem):
    series: str = ""
    issue_number: str = ""
    publisher: str = ""
    publication_year: int | None = None
    variant: str = ""
    grade: str = ""