from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Optional, Sequence

from inventory_app.shared.logging import get_logger, log_operation, LogLevels
from inventory_app.ingredients.exceptions import IngredientError, DuplicateIngredientError, UnknownIngredientError
from inventory_app.common.enums import ItemType
from inventory_app.ingredients.repositories.ingredient_repo import IngredientRepo
from inventory_app.ingredients.models import *
from inventory_app.ingredients.services.category_service import IngredientCategoryService
from inventory_app.ingredients.services.subcategory_service import IngredientSubcategoryService
from inventory_app.items.services.item_service import ItemService
from inventory_app.units.models import Unit
from inventory_app.units.services.unit_service import UnitService
from inventory_app.inventory.models import InventoryLocation
from inventory_app.inventory.services.location_service import InventoryLocationService


logger = get_logger(__name__)


class IngredientService:

    def __init__(self, session: Session):

        self.ingredient_repo = IngredientRepo(session)
        self.item_service = ItemService(session)
        self.category_service = IngredientCategoryService(session)
        self.subcategory_service = IngredientSubcategoryService(session)
        self.unit_service = UnitService(session)
        self.location_service = InventoryLocationService(session)

    def get_by_name(
            self,
            name: str
    ) -> Ingredient:

        ingredient = self.ingredient_repo.get_by_name(name)

        if ingredient is None:
            raise UnknownIngredientError(name)

        return ingredient


    def get_or_create(
            self,
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

        existing = self.ingredient_repo.get_by_name(name)

        if existing is not None:
            return existing

        item = self.item_service.create(name, ItemType.INGREDIENT)

        ing = Ingredient(
            item=item,
            category=category,
            subcategory=subcategory,
            location=location,
            base_unit=base_unit,
            count_unit=count_unit,
            purchase_unit=purchase_unit
        )

        ingredient = self.ingredient_repo.create(ing)

        return ingredient


    def get_all(
            self
    ) -> Sequence[Ingredient]:
        return self.ingredient_repo.get_all()


    def create_by_name(
            self,
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

        existing = self.ingredient_repo.get_by_name(name)

        if existing is not None:
            raise DuplicateIngredientError(f"Ingredient '{name}' already exists!")

        category_obj = self.category_service.get_by_name(category)
        subcategory_obj = self.subcategory_service.get_by_name(subcategory)
        base_obj = self.unit_service.get_by_name(base_unit)

        count_obj = None
        purchase_obj = None
        location_obj = None

        if count_unit is not None:
            count_obj = self.unit_service.get_by_name(count_unit)
        if purchase_unit is not None:
            purchase_obj = self.unit_service.get_by_name(purchase_unit)
        if location is not None:
            location_obj = self.location_service.get_by_name(location)

        item = self.item_service.create(name, ItemType.INGREDIENT)

        ing = Ingredient(
            item=item,
            category=category_obj,
            subcategory=subcategory_obj,
            location=location_obj,
            base_unit=base_obj,
            count_unit=count_obj,
            purchase_unit=purchase_obj
        )

        return self.ingredient_repo.create(ing)


    def create(
            self,
            name: str,
            category: IngredientCategory | str,
            subcategory: IngredientSubcategory | str,
            base_unit: Unit | str,
            count_unit: Unit | str,
            purchase_unit: Unit | str
    ) -> Ingredient:

        existing = self.ingredient_repo.get_by_name(name)

        if existing is not None:
            return existing

        category = self._resolve_category(category)
        subcategory = self._resolve_subcategory(subcategory)
        base_unit = self._resolve_unit(base_unit)
        count_unit = self._resolve_unit(count_unit)
        purchase_unit = self._resolve_unit(purchase_unit)

        item = self.item_service.create(name, ItemType.INGREDIENT)

        ing = Ingredient(
            item=item,
            category=category,
            subcategory=subcategory,
            base_unit=base_unit,
            count_unit=count_unit,
            purchase_unit=purchase_unit
        )

        ingredient = self.ingredient_repo.create(ing)

        return ingredient


    def _resolve_category(
            self,
            name: IngredientCategory | str
    ) -> IngredientCategory:
        if isinstance(name, IngredientCategory):
            return name
        else:
            return self.category_service.get_by_name(name)

    def _resolve_subcategory(
            self,
            name: IngredientSubcategory | str
    ) -> IngredientSubcategory:
        if isinstance(name, IngredientSubcategory):
            return name
        else:
            return self.subcategory_service.get_by_name(name)

    def _resolve_unit(
            self,
            name: Unit | str
    ) -> Unit:
        if isinstance(name, Unit):
            return name
        else:
            return self.unit_service.get_by_name_or_abbv(name)