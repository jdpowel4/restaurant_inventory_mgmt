from sqlalchemy import select
from sqlalchemy.orm import Session

from inventory_app.shared.logging import get_logger, log_operation, LogLevels
from inventory_app.ingredients.models import IngredientCategory, IngredientSubcategory

def get_by_name(
        session: Session,
        name: str
) -> IngredientSubcategory | None:
    
    stmt = select(IngredientSubcategory).where(IngredientSubcategory.name == name)

    return session.scalar(stmt)


def create(
        session: Session,
        subcategory: IngredientSubcategory
) -> IngredientSubcategory:
    
    session.add(subcategory)
    return subcategory