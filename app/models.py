from dataclasses import dataclass

@dataclass
class InventoryItem:
    id: int
    name: str
    category: str
    quantity: int
    location: str
    notes: str