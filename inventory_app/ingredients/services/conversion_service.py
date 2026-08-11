from sqlalchemy import Select
from sqlalchemy.orm import Session
from decimal import Decimal
from typing import Sequence

from inventory_app.shared.logging import get_logger, log_operation, LogLevels
from inventory_app.shared.exceptions import DuplicateConversionError
from inventory_app.units.models import Unit
from inventory_app.units.services.unit_service import UnitService
from inventory_app.ingredients.models import Ingredient, IngredientUnitConversion
from inventory_app.ingredients.services.ingredient_service import IngredientService
from inventory_app.ingredients.repositories.conversion_repo import IngredientConversionRepo

logger = get_logger(__name__)


class IngredientConversionService:

    def __init__(self, session: Session):

        self.conversion_repo = IngredientConversionRepo(session)
        self.ingredient_service = IngredientService(session)
        self.unit_service = UnitService(session)

    def create(
            self,
            ingredient: Ingredient,
            from_unit: Unit,
            to_unit: Unit,
            multiplier: Decimal
    ) -> IngredientUnitConversion:

        existing = self.conversion_repo.check_existing(
            ingredient=ingredient,
            from_unit=from_unit,
            to_unit=to_unit
        )

        if existing is not None:
            raise DuplicateConversionError(
                f"{ingredient.item.name}: {from_unit.name} -> {to_unit.name} already exists!"
            )

        conv = IngredientUnitConversion(
            ingredient=ingredient,
            from_unit=from_unit,
            to_unit=to_unit,
            multiplier=multiplier
        )

        logger.debug(
            "Creating Ingredient Conversion for:"
            f"{ingredient}: {from_unit} -> {to_unit}"
        )

        return self.conversion_repo.create(conv)

    def create_by_name(
            self,
            ingredient: str,
            from_unit: str,
            to_unit: str,
            multiplier: Decimal
    ) -> IngredientUnitConversion:

        ing_obj = self.ingredient_service.get_by_name(ingredient)
        from_obj = self.unit_service.get_by_name(from_unit)
        to_obj = self.unit_service.get_by_name(to_unit)

        existing = self.conversion_repo.check_existing(
            ing_obj,
            from_obj,
            to_obj,
        )

        if existing is not None:
            raise DuplicateConversionError(
                f"{ing_obj.item.name}: {from_obj.name} -> {to_obj.name} already exists!"
            )

        conv = IngredientUnitConversion(
            ingredient=ing_obj,
            from_unit=from_obj,
            to_unit=to_obj,
            multiplier=multiplier
        )

        return self.conversion_repo.create(conv)


    def get_by_ingredient(
            self,
            ingredient: Ingredient
    ) -> Sequence[IngredientUnitConversion]:
        return self.conversion_repo.get_ingredient_conversion(ingredient)