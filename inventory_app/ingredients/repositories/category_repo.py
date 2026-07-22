from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Sequence

from inventory_app.shared.logging import get_logger, log_operation, LogLevels

from inventory_app.ingredients.models import IngredientCategory

logger = get_logger(__name__)


def get_by_id():
    pass


def get_by_name(
        session: Session,
        name: str
    ) -> IngredientCategory | None:

    stmt = select(IngredientCategory).where(IngredientCategory.name == name)

    return session.scalar(stmt)


def get_all(
        session: Session
) -> Sequence[IngredientCategory]:
    stmt = select(IngredientCategory).order_by(IngredientCategory.name)
    return list(session.scalars(stmt))

log_operation()
def create(
        session: Session,
        name: str,
        sort_order: int
) -> IngredientCategory:
    
    category = IngredientCategory(name=name, sort_order=sort_order)

    session.add(category)

    return category