from sqlalchemy import select
from sqlalchemy.orm import Session
from decimal import Decimal

from inventory_app.shared.logging import get_logger, log_operation, LogLevels
from inventory_app.shared.exceptions import RecipeError, DuplicateRecipeComponentError
from inventory_app.recipes.repositories import component_repo
from inventory_app.recipes.services import recipe_service
from inventory_app.recipes.models import Recipe, RecipeComponent
from inventory_app.items.models import Item
from inventory_app.items.services import item_service
from inventory_app.units.models import Unit
from inventory_app.units.services import unit_service


def create(
        session: Session,
        recipe: Recipe,
        item: Item,
        quantity: Decimal,
        unit: Unit,
) -> RecipeComponent:
    
    existing = component_repo.get_component(session, recipe, item)

    if existing is not None:
        raise DuplicateRecipeComponentError(f"Recipe Component '{item.name}' already exists in Recipe '{recipe.item.name}'.")
    
    component = RecipeComponent(
        recipe=recipe,
        item=item,
        quantity=quantity,
        unit=unit
    )

    return component_repo.create(session, component)


def create_by_name(
        session: Session,
        recipe: str,
        item: str,
        quantity: Decimal,
        unit: str
) -> RecipeComponent:
    
    recipe_obj = recipe_service.get_by_name(session, recipe)
    item_obj = item_service.get_by_name(session, item)
    unit_obj = unit_service.get_by_name(session, unit)

    component = RecipeComponent(
        recipe=recipe_obj,
        item=item_obj,
        quantity=quantity,
        unit=unit_obj
    )

    return component_repo.create(session, component)




