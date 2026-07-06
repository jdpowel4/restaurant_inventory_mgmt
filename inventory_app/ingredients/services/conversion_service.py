from sqlalchemy import Select
from sqlalchemy.orm import Session

from inventory_app.shared.logging import get_logger, log_operation, LogLevels
from inventory_app.shared.exceptions import DuplicateConversionError
from inventory_app.units.models import Unit
from inventory_app.ingredients.models import Ingredient, IngredientUnitConversion
from inventory_app.ingredients.repositories import conversion_repo

logger = get_logger(__name__)

def create(
        session: Session,
        ingredient: Ingredient,
        from_unit: Unit,
        to_unit: Unit,
        multiplier: int
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