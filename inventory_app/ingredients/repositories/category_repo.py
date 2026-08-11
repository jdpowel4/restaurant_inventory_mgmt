from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Sequence

from inventory_app.shared.logging import get_logger, log_operation, LogLevels

from inventory_app.ingredients.models import IngredientCategory

logger = get_logger(__name__)

class IngredientCategoryRepo:

    def __init__(self, session: Session):

        self.session = session

    def get_by_name(
            self,
            name: str
        ) -> IngredientCategory | None:

        stmt = select(IngredientCategory).where(IngredientCategory.name == name)

        return self.session.scalar(stmt)


    def get_all(
            self
    ) -> Sequence[IngredientCategory]:
        stmt = select(IngredientCategory).order_by(IngredientCategory.name)
        return list(self.session.scalars(stmt))

    log_operation()
    def create(
            self,
            name: str,
            sort_order: int
    ) -> IngredientCategory:

        category = IngredientCategory(name=name, sort_order=sort_order)

        self.session.add(category)

        return category