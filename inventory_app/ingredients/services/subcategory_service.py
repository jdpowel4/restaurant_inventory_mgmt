from sqlalchemy.orm import Session
from typing import Sequence

from inventory_app.shared.logging import get_logger, log_operation, LogLevels
from inventory_app.ingredients.exceptions import UnknownSubcategoryError

from inventory_app.ingredients.models import IngredientSubcategory, IngredientCategory
from inventory_app.ingredients.repositories.subcategory_repo import IngredientSubcategoryRepo

logger = get_logger(__name__)


class IngredientSubcategoryService:

    def __init__(self, session: Session):

        self.subcategory_repo = IngredientSubcategoryRepo(session)

    def get_or_create(
            self,
            name: str,
            category: IngredientCategory
    ) -> IngredientSubcategory:

        existing = self.subcategory_repo.get_by_name(name)

        if existing is not None:
            return existing

        subcategory = IngredientSubcategory(
            name=name,
            category=category
        )

        return self.subcategory_repo.create(subcategory)


    def get_by_name(
            self,
            name: str
    ) -> IngredientSubcategory:

        subcategory = self.subcategory_repo.get_by_name(name)

        if subcategory is None:
            raise UnknownSubcategoryError(name)

        return subcategory


    def get_by_category_name(
            self,
            category: str
    ) -> Sequence[IngredientSubcategory]:
        return self.subcategory_repo.get_by_category_name(category)

    
    def get_all(
            self
    ) -> Sequence[IngredientSubcategory]:
        return self.subcategory_repo.get_all()