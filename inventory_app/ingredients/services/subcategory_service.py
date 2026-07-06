from sqlalchemy.orm import Session

from inventory_app.shared.logging import get_logger, log_operation, LogLevels

from inventory_app.ingredients.models import IngredientSubcategory, IngredientCategory
from inventory_app.ingredients.repositories import subcategory_repo

logger = get_logger(__name__)

def get_or_create(
        session: Session,
        name: str,
        category: IngredientCategory
) -> IngredientSubcategory:
    
    existing = subcategory_repo.get_by_name(session, name)

    if existing is not None:
        return existing
    
    subcategory = IngredientSubcategory(
        name=name,
        category=category
    )

    return subcategory_repo.create(session, subcategory)


def get_by_name(
        session: Session,
        name: str
) -> IngredientSubcategory | None:
    
    return subcategory_repo.get_by_name(session, name)