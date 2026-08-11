from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Sequence

from inventory_app.shared.logging import get_logger, log_operation, LogLevels
from inventory_app.ingredients.models import Ingredient
from inventory_app.items.models import Item

logger = get_logger(__name__)


class IngredientRepo:

    def __init__(self, session: Session):

        self.session = session

    def get_by_id(self):
        pass

    def get_by_name(
            self,
            name: str
    ) -> Ingredient | None:

        stmt = select(Ingredient).join(Ingredient.item).where(Item.name.ilike(name))

        return self.session.scalar(stmt)

    def get_all(
            self
    ) -> Sequence[Ingredient]:
        stmt = (select(Ingredient)
        .join(Ingredient.item)
        .order_by(Item.name))
        return list(self.session.scalars(stmt))

    def get_by_category(self):
        pass

    def search(self):
        pass

    def create(
            self,
            ingredient: Ingredient
    ) -> Ingredient:

        logger.debug(
            f"Creating Ingredient {ingredient.item}"
        )
        self.session.add(ingredient)

        return ingredient

    def delete(self):
        pass

