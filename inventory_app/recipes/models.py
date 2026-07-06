from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from inventory_app.units.models import Unit
    from inventory_app.ingredients.models import Item

from sqlalchemy import Boolean, ForeignKey, String, Numeric
from sqlalchemy.orm import relationship, Mapped, mapped_column
from decimal import Decimal

from inventory_app.common.base import Base
from inventory_app.common.mixins import TimestampMixin



class Recipe(Base, TimestampMixin):

    __tablename__ = "recipes"

    id: Mapped[int] = mapped_column(primary_key=True)
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id"), unique=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    yield_qty: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    yeild_unit_id: Mapped[int] = mapped_column(ForeignKey("units.id"))

    serving_qty: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    serving_unit_id: Mapped[int] = mapped_column(ForeignKey("units.id"))

    locked: Mapped[Boolean] = mapped_column(Boolean, default=False)

    costing_method: Mapped[str] = mapped_column(String, default="most_recent_cost")


    item: Mapped["Item"] = relationship(back_populates="recipe")
    yeild_unit: Mapped["Unit"] = relationship(foreign_keys=[yeild_unit_id])
    serving_unit: Mapped["Unit"] = relationship(foreign_keys=[serving_unit_id])
    components: Mapped[list["RecipeComponent"]] = relationship(back_populates="recipe", cascade="all, delete-orphan", uselist=True)


    def __repr__(self) -> str:
        return f"<Recipe(name='{self.name}')>"



class RecipeComponent(Base):

    __tablename__ = "recipe_components"

    id: Mapped[int] = mapped_column(primary_key=True)
    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipes.id"))
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id"))

    quantity: Mapped[Decimal] = mapped_column(Numeric(10, 2))

    unit_id: Mapped[int] = mapped_column(ForeignKey("units.id"))

    recipe: Mapped["Recipe"] = relationship(back_populates="components")
    item: Mapped["Item"] = relationship()
    unit: Mapped["Unit"] = relationship()


    def __repr__(self) -> str:
        return f"<RecipeComponent(name='{self.item.name}')>"
    

class RecipeProduction(Base, TimestampMixin):

    __tablename__ = "recipe_productions"

    id: Mapped[int] = mapped_column(primary_key=True)
    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipes.id"))
    quantity_produced: Mapped[Decimal] = mapped_column(Numeric(10, 2))

    recipe: Mapped["Recipe"] = relationship()