from sqlalchemy import select
from sqlalchemy.orm import Session

from inventory_app.units.models import *
from inventory_app.shared.logging import get_logger, log_operation


logger = get_logger(__name__)


def get_by_name(
        session: Session,
        name: str
) -> UnitCategory | None:
    
    logger.debug(
        f"Selecting UnitCategory: '{name}'"
    )
    stmt = select(UnitCategory).where(
        UnitCategory.name == name
    )

    return session.scalar(stmt)


@log_operation()
def create(
        session: Session,
        name: str
) -> UnitCategory:
    
    logger.debug(
        f"Creating Category: '{name}'"
    )

    category = UnitCategory(name=name)

    session.add(category)

    return category

