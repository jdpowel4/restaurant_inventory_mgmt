from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from inventory_app.recipes.models import Recipe
    from inventory_app.ingredients.models import Ingredient

from sqlalchemy import String
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from inventory_app.common.base import Base
from inventory_app.common.mixins import TimestampMixin
from inventory_app.common.enums import ItemType


class Item(Base, TimestampMixin):

    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    item_type: Mapped[ItemType] = mapped_column(
        SQLEnum(
            ItemType,
            native_enum=False
        ),
        nullable=False
    )
    

    ingredient: Mapped["Ingredient | None"] = relationship(back_populates="item")
    recipe: Mapped["Recipe | None"] = relationship(back_populates="item")


    def __repr__(self) -> str:
        return f"<Item(name='{self.name}')>"
    
    def __str__(self) -> str:
        return self.name