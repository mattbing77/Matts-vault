from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db_models import InventoryRecord, MagicCardRecord, ComicBookRecord


def create_item(
    session: Session,
    name: str,
    category: str,
    quantity: int = 1,
    location: str = "",
    notes: str = "",
) -> InventoryRecord:
    """Create and save a new inventory item."""

    if not name.strip():
        raise ValueError("Item name cannot be empty.")

    if quantity < 0:
        raise ValueError("Quantity cannot be negative.")

    item = InventoryRecord(
        name=name.strip(),
        category=category,
        quantity=quantity,
        location=location,
        notes=notes,
    )

    session.add(item)
    session.commit()
    session.refresh(item)

    return item


def get_all_items(session: Session) -> list[InventoryRecord]:
    """Retrieve all inventory items ordered by ID."""

    statement = select(InventoryRecord).order_by(InventoryRecord.id)

    return list(session.scalars(statement).all())
def get_item_by_id(
    session: Session,
    item_id: int,
) -> InventoryRecord | None:
    """Retrieve one inventory item by its ID."""

    return session.get(InventoryRecord, item_id)


def update_item(
    session: Session,
    item_id: int,
    name: str | None = None,
    category: str | None = None,
    quantity: int | None = None,
    location: str | None = None,
    notes: str | None = None,
) -> InventoryRecord | None:
    """Update an existing inventory item."""

    item = get_item_by_id(session, item_id)

    if item is None:
        return None

    if name is not None:
        if not name.strip():
            raise ValueError("Item name cannot be empty.")
        item.name = name.strip()

    if category is not None:
        item.category = category

    if quantity is not None:
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")
        item.quantity = quantity

    if location is not None:
        item.location = location

    if notes is not None:
        item.notes = notes

    session.commit()
    session.refresh(item)

    return item


def delete_item(session: Session, item_id: int) -> bool:
    """Delete an inventory item by ID."""

    item = get_item_by_id(session, item_id)

    if item is None:
        return False

    session.delete(item)
    session.commit()

    return True
def create_magic_card(
    session: Session,
    name: str,
    quantity: int = 1,
    location: str = "",
    notes: str = "",
    set_code: str = "",
    collector_number: str = "",
    finish: str = "Nonfoil",
    condition: str = "",
    deck_assignment: str = "",
) -> InventoryRecord:
    """Create a Magic card and its inventory record."""

    if not name.strip():
        raise ValueError("Card name cannot be empty.")

    if quantity < 0:
        raise ValueError("Quantity cannot be negative.")

    item = InventoryRecord(
        name=name.strip(),
        category="Magic Cards",
        quantity=quantity,
        location=location,
        notes=notes,
    )

    item.magic_card = MagicCardRecord(
        set_code=set_code,
        collector_number=collector_number,
        finish=finish,
        condition=condition,
        deck_assignment=deck_assignment,
    )

    session.add(item)
    session.commit()
    session.refresh(item)

    return item


def create_comic_book(
    session: Session,
    name: str,
    quantity: int = 1,
    location: str = "",
    notes: str = "",
    series: str = "",
    issue_number: str = "",
    publisher: str = "",
    publication_year: int | None = None,
    variant: str = "",
    grade: str = "",
) -> InventoryRecord:
    """Create a comic book and its inventory record."""

    if not name.strip():
        raise ValueError("Comic name cannot be empty.")

    if quantity < 0:
        raise ValueError("Quantity cannot be negative.")

    item = InventoryRecord(
        name=name.strip(),
        category="Comics",
        quantity=quantity,
        location=location,
        notes=notes,
    )

    item.comic_book = ComicBookRecord(
        series=series,
        issue_number=issue_number,
        publisher=publisher,
        publication_year=publication_year,
        variant=variant,
        grade=grade,
    )

    session.add(item)
    session.commit()
    session.refresh(item)

    return item