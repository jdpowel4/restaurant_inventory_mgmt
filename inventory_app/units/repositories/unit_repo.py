from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Sequence

from inventory_app.units.models import *
from inventory_app.shared.logging import get_logger, log_operation, LogLevels

logger = get_logger(__name__)


def get_by_id(
        session: Session,
        unit_id: int
    ) -> Unit | None:
    
    return session.get(Unit, unit_id)


def get_by_name(
        session: Session,
        name: str
) -> Unit | None:
    
    stmt = select(Unit).where(Unit.name == name)

    return session.scalar(stmt)


def get_by_abbreviation(
        session: Session,
        abbreviation: str
) -> Unit | None:
    
    stmt = select(Unit).where(Unit.abbreviation == abbreviation)

    return session.scalar(stmt)


def get_all(
        session: Session
) -> Sequence[Unit]:
    
    stmt = select(Unit).order_by(Unit.name)

    return list(session.scalars(stmt))


def create(
        session: Session,
        unit: Unit
) -> Unit:
    
    session.add(unit)

    return unit

