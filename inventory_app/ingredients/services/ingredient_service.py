from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Optional

from inventory_app.shared.logging import get_logger, log_operation, LogLevels
from inventory_app.common.enums import ItemType
from inventory_app.ingredients.repositories import ingredient_repo
from inventory_app.ingredients.models import *
from inventory_app.items.services import item_service
from inventory_app.units.models import Unit
from inventory_app.inventory.models import InventoryLocation

logger = get_logger(__name__)

def get_by_name(
        session: Session,
        name: str
) -> Ingredient | None:
    
    ingredient = select(Ingredient).where(Ingredient.item.name == name)

    return session.scalar(ingredient)


def get_or_create(
        session: Session,
        *,
        name: str,
        category: IngredientCategory,
        subcategory: IngredientSubcategory,
        base_unit: Unit,
        location: InventoryLocation | None = None,
        count_unit: Unit | None = None,
        purchase_unit: Unit | None = None
) -> Ingredient:
    
    existing = ingredient_repo.get_by_name(session, name)
    
    if existing is not None:
        return existing
    
    item = item_service.create(session, name, ItemType.INGREDIENT)

    ing = Ingredient(
        item=item,
        category=category,
        subcategory=subcategory,
        location=location,
        base_unit=base_unit,
        count_unit=count_unit,
        purchase_unit=purchase_unit
    )

    ingredient = ingredient_repo.create(session, ing)

    return ingredient