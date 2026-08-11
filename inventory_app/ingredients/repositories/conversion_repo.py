from sqlalchemy import select
from sqlalchemy.orm import Session

from inventory_app.shared.logging import get_logger
from inventory_app.ingredients.models import Ingredient, IngredientUnitConversion
from inventory_app.units.models import Unit

logger = get_logger(__name__)


class IngredientConversionRepo:

    def __init__(self, session: Session):

        self.session = session

    def get_ingredient_conversion(
            self,
            ingredient: Ingredient
    ) -> list[IngredientUnitConversion]:
        stmt = select(IngredientUnitConversion).where(
            IngredientUnitConversion.ingredient_id == ingredient.id
        )
        return list(self.session.scalars(stmt))


    def create(
            self,
            conversion: IngredientUnitConversion
    ) -> IngredientUnitConversion:

        logger.debug(
            "Creating Ingredient Conversion for:"
            f"{conversion.ingredient}: {conversion.from_unit} -> {conversion.to_unit}"
        )
        self.session.add(conversion)

        return conversion


    def check_existing(
            self,
            ingredient: Ingredient,
            from_unit: Unit,
            to_unit: Unit
    ) -> IngredientUnitConversion | None:


        logger.debug(
            "Checking for existing Ingredient Conversion for:"
            f"{ingredient}: {from_unit} -> {to_unit}"
        )
        stmt = select(IngredientUnitConversion).where(
            IngredientUnitConversion.ingredient == ingredient,
            IngredientUnitConversion.from_unit == from_unit,
            IngredientUnitConversion.to_unit == to_unit
        )

        return self.session.scalar(stmt)