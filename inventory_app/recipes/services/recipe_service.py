from sqlalchemy import select
from sqlalchemy.orm import Session
from decimal import Decimal
from datetime import datetime
from typing import List

from inventory_app.shared.logging import get_logger, log_operation, LogLevels
from inventory_app.recipes.exceptions import RecipeError, UnknownRecipeError, DuplicateRecipeError
from inventory_app.common.enums import ItemType
from inventory_app.shared.config import EXPORT_DIR
from inventory_app.recipes.repositories.recipe_repo import RecipeRepo
from inventory_app.recipes.engines.costing_engine import CostingEngine
from inventory_app.recipes.dto import ReportMetadata, RecipeInput, RecipeComponentInput
from inventory_app.recipes.models import Recipe
from inventory_app.recipes.reporting.exporters.pdf_exporter import PDFExporter
from inventory_app.recipes.reporting.templates.recipe_cost_template import RecipeCostTemplate
from inventory_app.recipes.exceptions import UnknownRecipeError
from inventory_app.recipes.services.component_service import RecipeComponentService
from inventory_app.units.models import Unit
from inventory_app.units.services.unit_service import UnitService
from inventory_app.items.services.item_service import ItemService
from inventory_app.items.models import Item


class RecipeService:

    def __init__(
            self,
            session: Session
    ):
        self.session = session
        self.recipe_repo = RecipeRepo(session)
        self.costing_engine = CostingEngine(session)
        self.item_service = ItemService(session)
        self.unit_service = UnitService(session)
        self.component_service = RecipeComponentService(session)

    def get_or_create(
            self,
            name: str,
            yield_qty: Decimal,
            yield_unit: Unit,
            serving_qty: Decimal,
            serving_unit: Unit
    ) -> Recipe:

        existing = self.recipe_repo.get_by_name(name)

        if existing is not None:
            return existing

        item = self.item_service.create(name, ItemType.RECIPE)

        rec = Recipe(
            item=item,
            yield_qty=yield_qty,
            yield_unit=yield_unit,
            serving_qty=serving_qty,
            serving_unit=serving_unit
        )

        recipe = self.recipe_repo.create(rec)

        return recipe


    def create_by_name(
            self,
            name: str,
            yield_qty: Decimal,
            yield_unit: str,
            serving_qty: Decimal,
            serving_unit: str
    ) -> Recipe:

        existing = self.recipe_repo.get_by_name(name)

        if existing is not None:
            raise DuplicateRecipeError(f"Recipe '{name}' already exist.")

        item = self.item_service.create(name, ItemType.RECIPE)

        yield_u = self.unit_service.get_by_name(yield_unit)
        serving_u = self.unit_service.get_by_name(serving_unit)

        recipe = Recipe(
            item=item,
            yield_qty=yield_qty,
            yield_unit=yield_u,
            serving_qty=serving_qty,
            serving_unit=serving_u
        )

        return self.recipe_repo.create(recipe)

    def get_by_name(
        self,
        recipe: str
    ) -> Recipe:
        rec = self.recipe_repo.get_by_name(recipe)
        if rec is None:
            raise UnknownRecipeError(f"Recipe '{recipe}' not found.")
        return rec


    def get(
        self,
        recipe: int | str
    ) -> Recipe:
        return self.recipe_repo.get(recipe)
    
    def export_recipe_report(
            self,
            recipe: str
    ):
        recipe_orm = self.get_by_name(recipe)
        report = self.costing_engine.cost_recipe(recipe_orm)

        metadata = ReportMetadata(
            title=f"{report.recipe_name} Cost Report",
            author="Jeremy Powell",
            subject="Recipe Cost Report",
            created=datetime.now(),
            company_name="Peggy's Kitchen Table",
            filename=str(EXPORT_DIR/f"{report.recipe_name}.pdf")
        )

        template = RecipeCostTemplate(report)

        PDFExporter().export(
            template=template,
            metadata=metadata,
        )

    def get_all(self):
        return self.recipe_repo.get_all()
    
    def update(
            self,
            recipe_id: int,
            data: RecipeInput
    ):
        recipe = self.recipe_repo.get(recipe_id)
        self._update_recipe(recipe, data)
        self._update_components(recipe, data.components)
        
    def _update_recipe(
            self,
            recipe: Recipe,
            data: RecipeInput
    ):
        if recipe is None:
            raise UnknownRecipeError(data.recipe_name)
        recipe.item.name = data.recipe_name
        recipe.yield_qty = data.yield_qty
        recipe.yield_unit_id = data.yield_unit_id
        recipe.serving_qty = data.serving_qty
        recipe.serving_unit_id = data.serving_unit_id
        
    def _update_components(self, recipe: Recipe, components: List[RecipeComponentInput]):
        for component in components:
            existing = {
                component.id: component
                for component in recipe.components
            }

            input_ids = set()

            if component.id is not None:
                input_ids.add(component.id)

                exist = existing.get(component.id)
                if exist is None:
                    raise ValueError(f"Component {component.id} does not belong to recipe {recipe.item.name}")

                exist.quantity = component.quantity
                exist.unit_id = component.unit_id
                exist.item_id = component.item_id
                
            else:
                self.component_service.create_from_input(recipe, component)
