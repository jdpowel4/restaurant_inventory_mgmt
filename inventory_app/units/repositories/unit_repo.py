from sqlalchemy import select, or_
from sqlalchemy.orm import Session
from typing import Sequence

from inventory_app.units.models import *
from inventory_app.shared.logging import get_logger, log_operation, LogLevels

logger = get_logger(__name__)


class UnitRepo:

    def __init__(self, session: Session):

        self.session = session

    def get_by_id(
            self,
            unit_id: int
        ) -> Unit | None:

        return self.session.get(Unit, unit_id)


    def get_by_name(
            self,
            name: str
    ) -> Unit | None:

        stmt = select(Unit).where(Unit.name == name)

        return self.session.scalar(stmt)


    def get_by_abbreviation(
            self,
            abbreviation: str
    ) -> Unit | None:

        stmt = select(Unit).where(Unit.abbreviation == abbreviation)

        return self.session.scalar(stmt)


    def get_all(
            self
    ) -> Sequence[Unit]:

        stmt = select(Unit).order_by(Unit.name)

        return list(self.session.scalars(stmt))


    def create(
            self,
            unit: Unit
    ) -> Unit:

        self.session.add(unit)

        return unit


    def get_by_name_or_abbv(
            self,
            value: str
    ) -> Unit | None:
        stmt = select(Unit).where(
            or_(
                Unit.name == value,
                Unit.abbreviation == value
            )
        )

        matches = list(self.session.scalars(stmt))

        match len(matches):
            case 0:
                return
            case 1:
                return matches[0]
        
