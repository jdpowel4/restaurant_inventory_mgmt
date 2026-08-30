from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Sequence

from inventory_app.shared.logging import get_logger, log_operation, LogLevels
from inventory_app.ingredients.models import IngredientCategory, IngredientSubcategory


class IngredientSubcategoryRepo:

    def __init__(self, session: Session):

        self.session = session


    def get_by_name(
            self,
            name: str
    ) -> IngredientSubcategory | None:

        stmt = select(IngredientSubcategory).where(IngredientSubcategory.name == name)

        return self.session.scalar(stmt)


    def create(
            self,
            subcategory: IngredientSubcategory
    ) -> IngredientSubcategory:

        self.session.add(subcategory)
        return subcategory


    def get_by_category_name(
            self,
            category: str
    ) -> Sequence[IngredientSubcategory]:
        stmt = (
            select(IngredientSubcategory)
            .join(IngredientCategory)
            .where(IngredientCategory.name==category)
        )
        return list(self.session.scalars(stmt))
    
    def get_all(self) -> Sequence[IngredientSubcategory]:
        stmt = select(IngredientSubcategory).order_by(IngredientSubcategory.name)
        return list(self.session.scalars(stmt))