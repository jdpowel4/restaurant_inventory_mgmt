from sqlalchemy import Select
from sqlalchemy.orm import Session
from decimal import Decimal
from typing import Sequence

from inventory_app.shared.logging import get_logger, log_operation, LogLevels
from inventory_app.shared.exceptions import DuplicateConversionError
from inventory_app.units.models import Unit
from inventory_app.units.services import unit_service
from inventory_app.ingredients.models import Ingredient, IngredientUnitConversion
from inventory_app.ingredients.services import ingredient_service
from inventory_app.ingredients.repositories import conversion_repo

logger = get_logger(__name__)

def create(
        session: Session,
        ingredient: Ingredient,
        from_unit: Unit,
        to_unit: Unit,
        multiplier: Decimal
) -> IngredientUnitConversion:
    
    existing = conversion_repo.check_existing(
        session=session,
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

    return conversion_repo.create(session, conv)

def create_by_name(
        session: Session,
        ingredient: str,
        from_unit: str,
        to_unit: str,
        multiplier: Decimal
) -> IngredientUnitConversion:
    
    ing_obj = ingredient_service.get_by_name(session, ingredient)
    from_obj = unit_service.get_by_name(session, from_unit)
    to_obj = unit_service.get_by_name(session, to_unit)
    
    existing = conversion_repo.check_existing(
        session,
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

    return conversion_repo.create(session, conv)


def get_by_ingredient(
        session: Session,
        ingredient: Ingredient
) -> Sequence[IngredientUnitConversion]:
    return conversion_repo.get_ingredient_conversion(session, ingredient)