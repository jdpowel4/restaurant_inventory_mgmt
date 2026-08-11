from sqlalchemy import select
from sqlalchemy.orm import Session
from decimal import Decimal

from inventory_app.shared.logging import get_logger, log_operation, LogLevels
from inventory_app.recipes.exceptions import DuplicateRecipeComponentError
from inventory_app.recipes.repositories.component_repo import RecipeComponentRepo
from inventory_app.recipes.services.recipe_service import RecipeService
from inventory_app.recipes.models import Recipe, RecipeComponent
from inventory_app.items.models import Item
from inventory_app.items.services.item_service import ItemService
from inventory_app.units.models import Unit
from inventory_app.units.services.unit_service import UnitService


class RecipeComponentService:

    def __init__(
            self,
            session
    ):
        self.session = session
        self.recipe_service = RecipeService(session)
        self.component_repo = RecipeComponentRepo(session)
        self.item_service = ItemService(session)
        self.unit_service = UnitService(session)
        

    def create(
            self,
            recipe: Recipe,
            item: Item,
            quantity: Decimal,
            unit: Unit,
    ) -> RecipeComponent:

        existing = self.component_repo.get_component(recipe, item)

        if existing is not None:
            raise DuplicateRecipeComponentError(f"Recipe Component '{item.name}' already exists in Recipe '{recipe.item.name}'.")

        component = RecipeComponent(
            recipe=recipe,
            item=item,
            quantity=quantity,
            unit=unit
        )

        return self.component_repo.create(component)


    def create_by_name(
            self,
            recipe: str,
            item: str,
            quantity: Decimal,
            unit: str
    ) -> RecipeComponent:
        
        # Grabbing ORM Objects from respective services.
        recipe_obj = self.recipe_service.get_by_name(recipe)
        item_obj = self.item_service.get_by_name(item)
        unit_obj = self.unit_service.get_by_name(unit)

        return self.create(recipe_obj, item_obj, quantity, unit_obj)




