from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Sequence

from inventory_app.shared.logging import get_logger, log_operation, LogLevels
from inventory_app.ingredients.models import Ingredient
from inventory_app.items.models import Item

logger = get_logger(__name__)


def get_by_id():
    pass


def get_by_name(
        session: Session,
        name: str
) -> Ingredient | None:
    
    stmt = select(Ingredient).join(Ingredient.item).where(Item.name == name)

    return session.scalar(stmt)



def get_all(
        session: Session
) -> Sequence[Ingredient]:
    stmt = (select(Ingredient)
    .join(Ingredient.item)
    .order_by(Item.name))
    return list(session.scalars(stmt))


def get_by_category():
    pass


def search():
    pass


def create(
        session: Session,
        ingredient: Ingredient
) -> Ingredient:
    
    logger.debug(
        f"Creating Ingredient {ingredient.item}"
    )
    session.add(ingredient)

    return ingredient


def delete():
    pass

