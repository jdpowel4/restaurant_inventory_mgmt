from sqlalchemy import select
from sqlalchemy.orm import Session
from decimal import Decimal
from datetime import datetime
from pathlib import Path

from inventory_app.shared.logging import get_logger, log_operation, LogLevels
from inventory_app.recipes.exceptions import RecipeError, UnknownRecipeError, DuplicateRecipeError
from inventory_app.common.enums import ItemType
from inventory_app.shared.config import EXPORT_DIR
from inventory_app.business.providers.business_provider import BusinessProvider
from inventory_app.recipes.repositories.recipe_repo import RecipeRepo
from inventory_app.recipes.engines.costing_engine import CostingEngine
from inventory_app.recipes.dto import ReportMetadata
from inventory_app.recipes.models import Recipe, RecipeComponent
from inventory_app.recipes.reporting.exporters.pdf_exporter import PDFExporter
from inventory_app.recipes.reporting.templates.recipe_cost_template import RecipeCostTemplate
from inventory_app.units.models import Unit
from inventory_app.units.services.unit_service import UnitService
from inventory_app.items.services.item_service import ItemService
from inventory_app.items.models import Item


class RecipeService:

    def __init__(
            self,
            session: Session
    ):
        self.recipe_repo = RecipeRepo(session)
        self.costing_engine = CostingEngine(session)
        self.item_service = ItemService(session)
        self.unit_service = UnitService(session)

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
        report = self.costing_engine.cost_recipe(recipe)

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