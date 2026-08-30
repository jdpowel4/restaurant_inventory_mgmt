from sqlalchemy.orm import Session
from decimal import Decimal

from inventory_app.common.conversions.conversion_engine import ConversionEngine
from inventory_app.recipes.dto import RecipeCostReport, ComponentCostLine, RecipeComponentInput, RecipeInput
from inventory_app.recipes.repositories.recipe_repo import RecipeRepo
from inventory_app.recipes.repositories.component_repo import RecipeComponentRepo
from inventory_app.recipes.models import Recipe, RecipeComponent
from inventory_app.ingredients.services.costing_service import IngredientCostService
from inventory_app.units.services.unit_service import UnitService
from inventory_app.items.services.item_service import ItemService


class CostingEngine:
   
    def __init__(self, session: Session):
        
        self.recipe_repo = RecipeRepo(session)
        self.conversion_engine = ConversionEngine(session)
        self.cost_service = IngredientCostService(session)
        self.unit_service = UnitService(session)
        self.item_service = ItemService(session)
        self.component_repo = RecipeComponentRepo(session)

    def cost_recipe(
            self,
            recipe: Recipe | RecipeInput | int,
            visited: set[tuple[str, int]] | None = None
    ) -> RecipeCostReport:
        if visited is None:
            visited = set()
        if isinstance(recipe, RecipeInput):
            return self._cost_recipe_input(recipe, visited)
        if isinstance(recipe, int):
            recipe = self.recipe_repo.get(recipe)
        if recipe is None:
            raise UnknownRecipeError(recipe)
        return self._cost_recipe_orm(recipe, visited)
        
    def _cost_recipe_input(
            self,
            recipe: RecipeInput,
            visited: set[tuple[str, int]]
    ) -> RecipeCostReport:
        
        key = self._get_visit_key(recipe)

        if key in visited:
            raise ValueError("Circular Recipe Reference")
        
        visited.add(key)
        try:
            total_cost = Decimal("0")

            yield_unit = self.unit_service.get(recipe.yield_unit_id)
            serving_unit = self.unit_service.get(recipe.serving_unit_id)

            yield_as_serving_units = self.conversion_engine.convert(
                recipe.yield_qty,
                yield_unit,
                serving_unit,
                ingredient=None,
                vendor_item=None
            )

            lines = []

            for component in recipe.components:
                line = self._cost_component_input(component, visited)

                total_cost += line.total_cost

                lines.append(line)


            total_servings = (yield_as_serving_units / recipe.serving_qty)

            cost_per_serving = (total_cost / total_servings)

            return RecipeCostReport(
                recipe_id=recipe.recipe_id,
                recipe_name=recipe.recipe_name,
                total_cost=total_cost,
                yield_qty=recipe.yield_qty,
                yield_unit=yield_unit.name,
                serving_qty=recipe.serving_qty,
                serving_unit=serving_unit.name,
                num_of_servings=total_servings,
                cost_per_yield_unit=(
                    total_cost / recipe.yield_qty
                ),
                cost_per_serving=cost_per_serving,
                component_lines=lines
            )
        
        finally:
            visited.remove(key)
            

    
    def _cost_recipe_orm(
            self,
            recipe: Recipe,
            visited: set[tuple[str, int]]
    ) -> RecipeCostReport:
       
        key = self._get_visit_key(recipe)

        if key in visited:
            raise ValueError("Circular Recipe Reference")

        visited.add(key)

        try:
            total_cost = Decimal("0")

            yield_as_serving_units = self.conversion_engine.convert(
                recipe.yield_qty,
                recipe.yield_unit,
                recipe.serving_unit,
                ingredient=None,
                vendor_item=None
            )

            lines = []

            for component in recipe.components:

                line = self._cost_component_orm(component, visited)

                total_cost += line.total_cost

                lines.append(line)


            total_servings = (yield_as_serving_units / recipe.serving_qty)

            cost_per_serving = (total_cost / total_servings)

            return RecipeCostReport(
                recipe_id=recipe.id,
                recipe_name=recipe.item.name,
                total_cost=total_cost,
                yield_qty=recipe.yield_qty,
                yield_unit=recipe.yield_unit.name,
                serving_qty=recipe.serving_qty,
                serving_unit=recipe.serving_unit.name,
                num_of_servings=total_servings,
                cost_per_yield_unit=(
                    total_cost / recipe.yield_qty
                ),
                cost_per_serving=cost_per_serving,
                component_lines=lines
            )
        
        finally:
            visited.remove(key)
    
    def _cost_component_input(
            self,
            component: RecipeComponentInput,
            visited
    ) -> ComponentCostLine:
        
        
        item = self.item_service.get(component.item_id)

        if item.ingredient:

            ingredient = item.ingredient

            unit_cost, vendor_item, source = (
                self.cost_service.get_cost(
                    ingredient.id,
                    method="most_recent_cost"
                )
            )
            unit = self.unit_service.get(component.unit_id)
            quantity = self.conversion_engine.convert(
                quantity=component.quantity,
                from_unit=unit,
                to_unit=ingredient.base_unit,
                ingredient=ingredient,
                vendor_item=vendor_item
            )

            total = quantity * unit_cost

            recipe_unit_cost = total / component.quantity

            return ComponentCostLine(
                component_id=0,
                component_name=item.name,
                recipe_quantity=component.quantity,
                recipe_unit=unit.name,
                recipe_unit_cost=recipe_unit_cost,
                total_cost=total,
                source=source
            )
        
        #
        # Sub Recipe
        #

        elif item.recipe:

            recipe = item.recipe

            report = self.cost_recipe(
                recipe.id,
                visited
            )
            unit = self.unit_service.get(component.unit_id)
            qty_in_yield_units = self.conversion_engine.convert(
                component.quantity,
                unit,
                recipe.yield_unit,
                ingredient=None,
                vendor_item=None
            )

            total = (
                qty_in_yield_units *
                report.cost_per_yield_unit
            )

            recipe_unit_cost = (
                total / component.quantity
            )

            return ComponentCostLine(
                component_id=0,
                component_name=item.name,
                recipe_quantity=component.quantity,
                recipe_unit=unit.name,
                recipe_unit_cost=recipe_unit_cost,
                total_cost=total,
                source="sub_recipe"
            )
        
        raise ValueError("Unknown Component Type.")
    
    def _cost_component_orm(
            self,
            component: RecipeComponent,
            visited: set[tuple[str, int]]
    ) -> ComponentCostLine:
        
        item = component.item

        #
        # Ingredient
        #

        if item.ingredient:

            ingredient = item.ingredient

            unit_cost, vendor_item, source = (
                self.cost_service.get_cost(
                    ingredient.id,
                    method=component.recipe.costing_method
                )
            )

            quantity = self.conversion_engine.convert(
                quantity=component.quantity,
                from_unit=component.unit,
                to_unit=ingredient.base_unit,
                ingredient=ingredient,
                vendor_item=vendor_item
            )

            total = quantity * unit_cost

            recipe_unit_cost = total / component.quantity

            return ComponentCostLine(
                component_id=component.id,
                component_name=item.name,
                recipe_quantity=component.quantity,
                recipe_unit=component.unit.name,
                recipe_unit_cost=recipe_unit_cost,
                total_cost=total,
                source=source
            )
        
        #
        # Sub Recipe
        #

        elif item.recipe:

            recipe = item.recipe

            report = self.cost_recipe(
                recipe.id,
                visited
            )

            qty_in_yield_units = self.conversion_engine.convert(
                component.quantity,
                component.unit,
                recipe.yield_unit,
                ingredient=None,
                vendor_item=None
            )

            total = (
                qty_in_yield_units *
                report.cost_per_yield_unit
            )

            recipe_unit_cost = (
                total / component.quantity
            )

            return ComponentCostLine(
                component_id=component.id,
                component_name=item.name,
                recipe_quantity=component.quantity,
                recipe_unit=component.unit.name,
                recipe_unit_cost=recipe_unit_cost,
                total_cost=total,
                source="sub_recipe"
            )
        
        raise ValueError("Unknown Component Type.")
    
    def _get_visit_key(self, recipe: RecipeInput | Recipe) -> tuple[str, int]:
        if isinstance(recipe, Recipe):
            return ("recipe", recipe.id)
        if recipe.recipe_id is not None:
            return ("recipe", recipe.recipe_id)
        return ("unsaved", id(recipe))
