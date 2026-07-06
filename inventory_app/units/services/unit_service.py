from sqlalchemy import select
from sqlalchemy.orm import Session
from decimal import Decimal
from collections.abc import Sequence

from inventory_app.shared.logging import get_logger, log_operation, LogLevels
from inventory_app.units.repositories import unit_repo
from inventory_app.units.models import Unit, UnitCategory


logger = get_logger(__name__)


def get_or_create(
        session: Session,
        name: str,
        category: UnitCategory,
        factor: Decimal,
        allow: bool,
        abbv: str | None = None
        
) -> Unit:
    
    existing = unit_repo.get_by_name(session, name)

    if existing is not None:
        return existing
    
    unit = Unit(
        name=name,
        abbreviation=abbv,
        category=category,
        factor=factor,
        allow_global_conversions=bool(allow)
    )
    return unit_repo.create(session, unit)


def get_all(
        session: Session
) -> Sequence[Unit]:
    return unit_repo.get_all(session)