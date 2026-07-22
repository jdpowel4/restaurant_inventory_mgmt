from sqlalchemy import select
from sqlalchemy.orm import Session
from decimal import Decimal
from collections.abc import Sequence

from inventory_app.shared.logging import get_logger, log_operation, LogLevels
from inventory_app.shared.exceptions import UnknownUnitError
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



def get_by_name(
        session: Session,
        name: str
) -> Unit:
    
    unit = unit_repo.get_by_name(session, name)

    if unit is None:
        raise UnknownUnitError(name)
    
    return unit

def get_by_abbv(
        session: Session,
        abbv: str
) -> Unit:
    unit = unit_repo.get_by_abbreviation(session, abbv)
    if unit is None:
        raise UnknownUnitError(abbv)
    return unit

def get_by_name_or_abbv(
        session: Session,
        value: str
) -> Unit:
    unit = unit_repo.get_by_name_or_abbv(session, value.lower())
    if unit is None:
        raise UnknownUnitError(value)
    return unit