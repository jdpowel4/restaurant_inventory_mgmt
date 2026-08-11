from sqlalchemy import select
from sqlalchemy.orm import Session
from decimal import Decimal
from collections.abc import Sequence

from inventory_app.shared.logging import get_logger, log_operation, LogLevels
from inventory_app.shared.exceptions import UnknownUnitError
from inventory_app.units.repositories.unit_repo import UnitRepo
from inventory_app.units.models import Unit, UnitCategory


logger = get_logger(__name__)


class UnitService:

    def __init__(self, session: Session):

        self.unit_repo = UnitRepo(session)

    def get_or_create(
            self,
            name: str,
            category: UnitCategory,
            factor: Decimal,
            allow: bool,
            abbv: str | None = None

    ) -> Unit:

        existing = self.unit_repo.get_by_name(name)

        if existing is not None:
            return existing

        unit = Unit(
            name=name,
            abbreviation=abbv,
            category=category,
            factor=factor,
            allow_global_conversions=bool(allow)
        )
        return self.unit_repo.create(unit)


    def get_all(
            self
    ) -> Sequence[Unit]:
        return self.unit_repo.get_all()



    def get_by_name(
            self,
            name: str
    ) -> Unit:

        unit = self.unit_repo.get_by_name(name)

        if unit is None:
            raise UnknownUnitError(name)

        return unit

    def get_by_abbv(
            self,
            abbv: str
    ) -> Unit:
        unit = self.unit_repo.get_by_abbreviation(abbv)
        if unit is None:
            raise UnknownUnitError(abbv)
        return unit

    def get_by_name_or_abbv(
            self,
            value: str
    ) -> Unit:
        unit = self.unit_repo.get_by_name_or_abbv(value.lower())
        if unit is None:
            raise UnknownUnitError(value)
        return unit