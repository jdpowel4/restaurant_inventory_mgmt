from sqlalchemy import select
from sqlalchemy.orm import Session
from decimal import Decimal

from inventory_app.shared.logging import get_logger, log_operation, LogLevels
from inventory_app.shared.exceptions import RecipeError, UnknownRecipeError
from inventory_app.common.enums import ItemType
from inventory_app.recipes.repositories import recipe_repo
from inventory_app.recipes.models import Recipe, RecipeComponent
from inventory_app.units.models import Unit
from inventory_app.units.services import unit_service
from inventory_app.items.services import item_service
from inventory_app.items.models import Item



def get_or_create(
        session: Session,
        name: str,
        yield_qty: Decimal,
        yield_unit: Unit,
        serving_qty: Decimal,
        serving_unit: Unit
) -> Recipe:
    
    existing = recipe_repo.get_by_name(session, name)

    if existing is not None:
        return existing
    
    item = item_service.create(session, name, ItemType.RECIPE)

    rec = Recipe(
        item=item,
        name=name,
        yield_qty=yield_qty,
        yield_unit=yield_unit,
        serving_qty=serving_qty,
        serving_unit=serving_unit
    )

    recipe = recipe_repo.create(session, rec)

    return recipe


def create_by_name(
        session: Session,
        name: str,
        yield_qty: Decimal,
        yield_unit: str,
        serving_qty: Decimal,
        serving_unit: str
) -> Recipe:
    
    existing = recipe_repo.get_by_name(session, name)

    if existing is not None:
        raise UnknownRecipeError(f"Recipe '{name}' does not exist.")
    
    item = item_service.create(session, name, ItemType.RECIPE)

    yield_u = unit_service.get_by_name(session, yield_unit)
    serving_u = unit_service.get_by_name(session, serving_unit)

    recipe = Recipe(
        item=item,
        yield_qty=yield_qty,
        yield_unit=yield_u,
        serving_qty=serving_qty,
        serving_unit=serving_u
    )

    return recipe_repo.create(session, recipe)

def get_by_name(
    session: Session,
    recipe: str
) -> Recipe | None:
    stmt = (select(Recipe)
        .join(Recipe.item)
        .where(Item.name == recipe)
    )
    return 