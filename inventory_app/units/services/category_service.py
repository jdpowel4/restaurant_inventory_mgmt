from sqlalchemy.orm import Session

from inventory_app.shared.logging import get_logger, log_operation, LogLevels
from inventory_app.units.models import *
from inventory_app.units.repositories.category_repo import UnitCategoryRepo

class UnitCategoryService:

    def __init__(self, session: Session):

        self.category_repo = UnitCategoryRepo(session)

    def get_or_create(
            self,
            name: str
    ) -> UnitCategory:

        category = self.category_repo.get_by_name(name)

        if category is not None:
            return category

        return self.category_repo.create(name)

