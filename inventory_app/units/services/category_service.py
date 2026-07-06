from sqlalchemy.orm import Session

from inventory_app.shared.logging import get_logger, log_operation, LogLevels
from inventory_app.units.models import *
from inventory_app.units.repositories import category_repo


def get_or_create(
        session: Session,
        name: str
) -> UnitCategory:
    
    category = category_repo.get_by_name(session, name)

    if category is not None:
        return category

    return category_repo.create(session, name)

