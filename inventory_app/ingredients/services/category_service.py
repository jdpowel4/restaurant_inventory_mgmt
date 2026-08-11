from sqlalchemy.orm import Session
from typing import Sequence

from inventory_app.shared.logging import get_logger, log_operation, LogLevels
from inventory_app.ingredients.exceptions import UnknownCategoryError

from inventory_app.ingredients.models import *
from inventory_app.ingredients.repositories.category_repo import IngredientCategoryRepo

class IngredientCategoryService:

    def __init__(self, session: Session):

        self.category_repo = IngredientCategoryRepo(session)

    def get_or_create(
            self,
            name: str,
            sort: int
    ) -> IngredientCategory:

        category = self.category_repo.get_by_name(name)

        if category is not None:
            return category

        return self.category_repo.create(name, sort)


    def get_by_name(
            self,
            name: str,
    ) -> IngredientCategory:

        category = self.category_repo.get_by_name(name)

        if category is None:
            raise UnknownCategoryError(name)

        return category

    def get_all(
            self
    ) -> Sequence[IngredientCategory]:
        return self.category_repo.get_all()
