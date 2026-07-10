from sqlalchemy import select
from sqlalchemy.orm import Session

from inventory_app.shared.logging import get_logger, log_operation, LogLevels
from inventory_app.recipes.models import Recipe
from inventory_app.items.models import Item

logger = get_logger(__name__)

def get_by_name(
        session: Session,
        name: str
) -> Recipe | None:
    stmt = (select(Recipe)
        .join(Recipe.item)
        .where(Item.name == name))
    return session.scalar(stmt)


def create(
        session: Session,
        recipe: Recipe
) -> Recipe:
    
    session.add(recipe)
    return recipe