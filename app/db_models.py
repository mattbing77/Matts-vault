from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class InventoryRecord(Base):
    __tablename__ = "inventory_items"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    location: Mapped[str] = mapped_column(String(255), default="", nullable=False)
    notes: Mapped[str] = mapped_column(Text, default="", nullable=False)

    magic_card: Mapped["MagicCardRecord | None"] = relationship(
        back_populates="inventory_item",
        uselist=False,
        cascade="all, delete-orphan",
    )

    comic_book: Mapped["ComicBookRecord | None"] = relationship(
        back_populates="inventory_item",
        uselist=False,
        cascade="all, delete-orphan",
    )
    images: Mapped[list["ItemImageRecord"]] = relationship(
        back_populates="inventory_item",
        cascade="all, delete-orphan",
    )
class MagicCardRecord(Base):
    __tablename__ = "magic_cards"

    item_id: Mapped[int] = mapped_column(
        ForeignKey("inventory_items.id"),
        primary_key=True,
    )

    set_code: Mapped[str] = mapped_column(String(20), default="")
    collector_number: Mapped[str] = mapped_column(String(30), default="")
    finish: Mapped[str] = mapped_column(String(30), default="Nonfoil")
    condition: Mapped[str] = mapped_column(String(50), default="")
    deck_assignment: Mapped[str] = mapped_column(String(255), default="")

    inventory_item: Mapped["InventoryRecord"] = relationship(
        back_populates="magic_card",
    )


class ComicBookRecord(Base):
    __tablename__ = "comic_books"

    item_id: Mapped[int] = mapped_column(
        ForeignKey("inventory_items.id"),
        primary_key=True,
    )

    series: Mapped[str] = mapped_column(String(255), default="")
    issue_number: Mapped[str] = mapped_column(String(30), default="")
    publisher: Mapped[str] = mapped_column(String(100), default="")
    publication_year: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )
    variant: Mapped[str] = mapped_column(String(255), default="")
    grade: Mapped[str] = mapped_column(String(50), default="")

    inventory_item: Mapped["InventoryRecord"] = relationship(
        back_populates="comic_book",
    )
class ItemImageRecord(Base):
    __tablename__ = "item_images"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    item_id: Mapped[int] = mapped_column(
        ForeignKey("inventory_items.id"),
        nullable=False,
    )

    storage_key: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    is_primary: Mapped[bool] = mapped_column(
        default=False,
        nullable=False,
    )

    inventory_item: Mapped["InventoryRecord"] = relationship(
        back_populates="images",
    )