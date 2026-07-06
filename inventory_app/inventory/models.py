from typing import TYPE_CHECKING

if TYPE_CHECKING:

    from inventory_app.ingredients.models import Ingredient
    from inventory_app.recipes.models import Recipe
    from inventory_app.purchases.models import Purchase, PurchaseItem

from sqlalchemy import String, ForeignKey, Numeric, CheckConstraint, Index, Text
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from decimal import Decimal

from inventory_app.common.base import Base
from inventory_app.common.mixins import TimestampMixin
from inventory_app.common.enums import EventType



class InventoryLocation(Base):

    __tablename__ = "inventory_locations"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)


    lots: Mapped[list["InventoryLot"]] = relationship(back_populates="location", uselist=True)
    ingredients: Mapped[list["Ingredient"]] = relationship(back_populates="location", uselist=True)


    def __repr__(self) -> str:
        return f"<InventoryLocation(name='{self.name}')>"
    

class InventoryLot(Base, TimestampMixin):
    
    __tablename__ = "inventory_lots"

    id: Mapped[int] = mapped_column(primary_key=True)
    event_id: Mapped[int] = mapped_column(ForeignKey("inventory_events.id"))
    ingredient_id: Mapped[int] = mapped_column(ForeignKey("ingredients.id"))
    purchase_item_id: Mapped[int] = mapped_column(ForeignKey("purchase_items.id"))
    location_id: Mapped[int] = mapped_column(ForeignKey("inventory_locations.id"))

    original_qty: Mapped[Decimal] = mapped_column(Numeric(10, 4), nullable=False)
    remaining_qty: Mapped[Decimal] = mapped_column(Numeric(10, 4), nullable=False)

    base_unit_cost: Mapped[Decimal] = mapped_column(Numeric(10, 4), nullable=False)


    __table_args__ = (
        CheckConstraint("remaining_qty >= 0"),
        CheckConstraint("original_qty >= 0")
    )


    event: Mapped["InventoryEvent"] = relationship()
    ingredient: Mapped["Ingredient"] = relationship(back_populates="lots")
    location: Mapped["InventoryLocation"] = relationship(back_populates="lots")
    purchase_item: Mapped["PurchaseItem"] = relationship(back_populates="lots")


class InventoryTransaction(Base, TimestampMixin):

    __tablename__ = "inventory_transactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    event_id: Mapped[int] = mapped_column(ForeignKey("inventory_events.id"))
    ingredient_id: Mapped[int] = mapped_column(ForeignKey("ingredients.id"))
    lot_id: Mapped[int] = mapped_column(ForeignKey("inventory_lots.id"))

    transaction_type: Mapped[str] = mapped_column(String, nullable=False)

    qty_change: Mapped[Decimal] = mapped_column(Numeric(10, 4), nullable=False)


    __table_args__ = (
        CheckConstraint("qty_change != 0"),
        Index("ix_inventory_transactions_ingredient_id", "ingredient_id")
    )

    ingredient: Mapped["Ingredient"] = relationship()
    lot: Mapped["InventoryLot"] = relationship()
    event: Mapped["InventoryEvent"] = relationship()

    
    def __repr__(self) -> str:
        return f"<InventoryTransaction(Type={self.transaction_type}, Ingredient={self.ingredient_id}, Qty={self.qty_change})>"
    


class InventoryEvent(Base, TimestampMixin):

    __tablename__ = "inventory_events"

    id: Mapped[int] = mapped_column(primary_key=True)

    event_type: Mapped[EventType] = mapped_column(
        SQLEnum(
            EventType,
            native_enum=False
        ),
        nullable=False
    )

    reference_type: Mapped[str] = mapped_column(String)
    reference_id: Mapped[int] = mapped_column()
    purchase_id: Mapped[int | None] = mapped_column(ForeignKey("purchases.id"), nullable=True)
    recipe_id: Mapped[int | None] = mapped_column(ForeignKey("recipes.id"), nullable=True)

    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    purchase: Mapped["Purchase"] = relationship()
    recipe: Mapped["Recipe"] = relationship()
