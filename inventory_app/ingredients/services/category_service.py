from sqlalchemy.orm import Session

from inventory_app.shared.logging import get_logger, log_operation, LogLevels
from inventory_app.shared.exceptions import UnknownCategoryError

from inventory_app.ingredients.models import *
from inventory_app.ingredients.repositories import category_repo

def get_or_create(
        session: Session,
        name: str,
        sort: int
) -> IngredientCategory:
    
    category = category_repo.get_by_name(session, name)

    if category is not None:
        return category
    
    return category_repo.create(session, name, sort)


def get_by_name(
        session: Session,
        name: str,
) -> IngredientCategory:
    
    category = category_repo.get_by_name(session, name)

    if category is None:
        raise UnknownCategoryError(name)
    
    return category
