from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from inventory_app.inventory.models import InventoryLot, InventoryLocation
    from inventory_app.vendors.models import VendorItem
    from inventory_app.units.models import Unit
    from inventory_app.items.models import Item

from sqlalchemy import String, ForeignKey, Numeric, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from decimal import Decimal

from inventory_app.common.base import Base
from inventory_app.common.mixins import TimestampMixin


class Ingredient(Base, TimestampMixin):

    __tablename__ = "ingredients"

    id: Mapped[int] = mapped_column(primary_key=True)
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id"), unique=True, nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("ingredient_categories.id"))
    subcategory_id: Mapped[int] = mapped_column(ForeignKey("ingredient_subcategories.id"))
    location_id: Mapped[int | None] = mapped_column(ForeignKey("inventory_locations.id"), nullable=True)
    base_unit_id: Mapped[int] = mapped_column(ForeignKey("units.id"))
    count_unit_id: Mapped[int | None] = mapped_column(ForeignKey("units.id"), nullable=True)
    purchase_unit_id: Mapped[int | None] = mapped_column(ForeignKey("units.id"), nullable=True)

    
    item: Mapped["Item"] = relationship(back_populates="ingredient")
    category: Mapped["IngredientCategory"] = relationship(back_populates="ingredient")
    subcategory: Mapped["IngredientSubcategory"] = relationship(back_populates="ingredients")
    location: Mapped["InventoryLocation"] = relationship(back_populates="ingredients")
    vendor_items: Mapped[list["VendorItem"]] = relationship(back_populates="ingredient", uselist=True)
    base_unit: Mapped["Unit"] = relationship(foreign_keys=[base_unit_id])
    count_unit: Mapped["Unit"] = relationship(foreign_keys=[count_unit_id])
    purchase_unit: Mapped["Unit"] = relationship(foreign_keys=[purchase_unit_id])
    lots: Mapped[list["InventoryLot"]] = relationship(back_populates="ingredient", uselist=True)


    def __repr__(self):
        return f"<Ingredient(name='{self.item.name}')>"


    def __str__(self):
        return self.item.name



class IngredientCategory(Base):

    __tablename__ = "ingredient_categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    sort_order: Mapped[int | None] = mapped_column(nullable=True)


    subcategory: Mapped[list["IngredientSubcategory"]] = relationship(back_populates="category", cascade="all, delete-orphan", uselist=True)
    ingredient: Mapped[list["Ingredient"]] = relationship(back_populates="category", uselist=True)

    def __repr__(self):
        return f"<IngredientCategory(name='{self.name}')>"
    
    def __str__(self): # type: ignore
        return self.name
    


class IngredientSubcategory(Base):

    __tablename__ = "ingredient_subcategories"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("ingredient_categories.id"), nullable=False)
    sort_order: Mapped[int | None] = mapped_column(nullable=True)

    
    category: Mapped["IngredientCategory"] = relationship(back_populates="subcategory")
    ingredients: Mapped[list["Ingredient"]] = relationship(back_populates="subcategory", uselist=True)


    def __repr__(self):
        return f"<IngredientSubcategory(name='{self.name}')>"

    def __str__(self): # type: ignore
        return self.name



class IngredientUnitConversion(Base):

    __tablename__ = "ingredient_unit_conversions"

    id: Mapped[int] = mapped_column(primary_key=True)
    ingredient_id: Mapped[int] = mapped_column(ForeignKey("ingredients.id"), nullable=False)
    from_unit_id: Mapped[int] = mapped_column(ForeignKey("units.id"), nullable=False)
    to_unit_id: Mapped[int] = mapped_column(ForeignKey("units.id"), nullable=False)
    multiplier: Mapped[Decimal] = mapped_column(Numeric(10,2), nullable=False)


    ingredient: Mapped["Ingredient"] = relationship()
    from_unit: Mapped["Unit"] = relationship(foreign_keys=[from_unit_id])
    to_unit: Mapped["Unit"] = relationship(foreign_keys=[to_unit_id])


    __table_args__ = (
        UniqueConstraint(
            "ingredient_id",
            "from_unit_id",
            "to_unit_id",
            name="uq_ingredient_unit_conversion"
        ),
    )

    def __repr__(self):
        return (
            f"<IngredientConversion ingredient='{self.ingredient_id} "
            f"{self.from_unit.name} -> {self.to_unit.name} x {self.multiplier}>"
        )