from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Optional, Sequence

from inventory_app.shared.logging import get_logger, log_operation, LogLevels
from inventory_app.shared.exceptions import IngredientError, DuplicateIngredientError, UnknownIngredientError
from inventory_app.common.enums import ItemType
from inventory_app.ingredients.repositories import ingredient_repo
from inventory_app.ingredients.models import *
from inventory_app.ingredients.services import category_service, subcategory_service
from inventory_app.items.services import item_service
from inventory_app.units.models import Unit
from inventory_app.units.services import unit_service
from inventory_app.inventory.models import InventoryLocation
from inventory_app.inventory.services import location_service


logger = get_logger(__name__)

def get_by_name(
        session: Session,
        name: str
) -> Ingredient:
    
    ingredient = ingredient_repo.get_by_name(session, name)

    if ingredient is None:
        raise UnknownIngredientError(name)
    
    return ingredient


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
    """
    Retrieves an existing ingredient by name or creates one.

    Args:
        session: Active SQLAlchemy session
        name: Ingredient Name
        category: Ingredient Category
        subcategory: Ingredient Subcategory
        base_unit: Base inventory unit
        count_unit: Optional counting unit
        purchase_unit: Optional purchasing unit
        location: Optional default storage location

    Returns:
        The existing or newly created Ingredient Object
    """
    
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


def get_all(
        session: Session
) -> Sequence[Ingredient]:
    return ingredient_repo.get_all(session)


def create_by_name(
        session: Session,
        name: str,
        category: str,
        subcategory: str,
        base_unit: str,
        count_unit: str | None,
        purchase_unit: str | None,
        location: str | None
) -> Ingredient:
    """
    Creates Ingredient from string values.
    """

    existing = ingredient_repo.get_by_name(session, name)

    if existing is not None:
        raise DuplicateIngredientError(f"Ingredient '{name}' already exists!")
    
    category_obj = category_service.get_by_name(session, category)
    subcategory_obj = subcategory_service.get_by_name(session, subcategory)
    base_obj = unit_service.get_by_name(session, base_unit)
    
    count_obj = None
    purchase_obj = None
    location_obj = None

    if count_unit is not None:
        count_obj = unit_service.get_by_name(session, count_unit)
    if purchase_unit is not None:
        purchase_obj = unit_service.get_by_name(session, purchase_unit)
    if location is not None:
        location_obj = location_service.get_by_name(session, location)

    item = item_service.create(session, name, ItemType.INGREDIENT)

    ing = Ingredient(
        item=item,
        category=category_obj,
        subcategory=subcategory_obj,
        location=location_obj,
        base_unit=base_obj,
        count_unit=count_obj,
        purchase_unit=purchase_obj
    )

    return ingredient_repo.create(session, ing)
