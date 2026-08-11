from sqlalchemy.orm import Session
from decimal import Decimal

from inventory_app.common.conversions.conversion_engine import ConversionEngine
from inventory_app.recipes.dto import RecipeCostReport, ComponentCostLine
from inventory_app.recipes.repositories.recipe_repo import RecipeRepo
from inventory_app.ingredients.services.costing_service import IngredientCostService


class CostingEngine:
    """
    Calculates the total cost of a recipe and produces a structured RecipeCostReport containing both the overall recipe cost and the individual cost of each recipe component.

    ------------------------------------------------------------------------------
    RESPONSIBILITY
    ------------------------------------------------------------------------------

    This class is intentionally responsible for the *calculation* of recipe cost, rather than for creating, updating, or otherwise managing recipes.

    The engine coordinates several existing components:

        RecipeRepo
            Retrieves recipe from the database.
        
        ConversionEngine
            Converts recipe component quantities into the ingredient's appropate base unit before costing.
        
        IngredientCostService
            Determins the monetary cost of a recipe component according to the requested costing method.

    ------------------------------------------------------------------------------
    RECURSIVE RECIPE COSTING
    ------------------------------------------------------------------------------

    Recipes may contain other recipes as components.

    for example:
        
        BBQ Plate
            ├── Pulled Pork
            ├── Coleslaw
            └── BBQ Sauce
                └── Tomato Sauce
                └── ...
            
    Because a recipe can contain another recipe, cost_recipe() calls itself recursively when it encounters a sub-recipe.

    The 'visited' set is used to detect circular recipe references.

    Example of an invalid circular relationship:

        Recipe A 
            └── Recipe B 
                └── Recipe A

    Without circular-reference detection, tthe recursive calls would continue indefinitely until Python eventually raised a RecursionError.

    The 'visited' set stores recipe IDs that are currently being evaluated. Before costing a recipe, its ID is checked against this set. If it is already present, a circular recipe relationship exists and the operation is stopped.

    ------------------------------------------------------------------------------
    SESSION / DATABASE RESPONSIBILITY
    ------------------------------------------------------------------------------

    The engine receives an existing SQLAlchemy Session rather than creating its own session.

    This is intentional. The caller owns the session and transaction boundary, while this engine simply uses that session through its repositories and services.

    This also allows the recipe repository, conversion engine, and ingredient cost service to participate in the same database operation/session. """

    def __init__(self, session: Session):
        """ 
        Initialize the costing engine and its required dependencies.
        
        Parameters
        ---------- 
        session: 

            The SQLAlchemy Session that should be used for all database operations performed by this costing operation. 
        
        The engine does not create or close the session. Session lifecycle remains the responsibility of the caller. 
        """        

        # RecipeRepo is deliberately used instead of RecipeService.
        #
        # This is an important architectural decision.
        #
        # RecipeService itself depends on CostingEngine. If CostingEngine
        # also depended on RecipeService, the dependancy graph would become:
        #
        #   RecipeService
        #        ↓
        #   CostingEngine
        #        ↓
        #   RecipeService
        #
        # This creates a circular dependency and therefore a circular import.
        #
        # The costing engine only needs to retrieve recipes; it does not need
        # the higher-level recipe service. Therefore, the repository is the
        # appropiate dependancy here.
        self.recipe_repo = RecipeRepo(session)

        # ConversionEngine converts a recipe component's quantity from the 
        # unit used by the recipe into the ingredient's base unit.
        #
        #Example:
        #
        #   Recipe calls for 2 cups of sauce.
        #   Ingredient base unit is fluid ounces.
        #
        # The conversion engine hendles the conversion before monetary
        # costing is preformed.
        self.conversion_engine = ConversionEngine(session)

        # IngredientCostService determins the monetary cost associated with
        # an ingredient.
        #
        # The costing engine is intentionally not responsible for determining
        # where ingredient prices come from. That responsibility belongs to 
        # IngredientCostService.
        self.cost_service = IngredientCostService(session)
    

    def cost_recipe(
            self,
            recipe,
            visited: set[int] | None = None
    ) -> RecipeCostReport:
        """
        Calculate the complete cost of a recipe.

        Parameters
        ----------
        recipe:
            The recipe identifier or other recipe reference accecpted by RecipeRepo.get().
        
        visited:
            A set containing recipe IDs that are already being evaluated higher in the current recursive call chain.

            This parameter is normally omitted by the caller. The first invocation creates the set, and recursive calls pass the same set downward.

        Returns
        ----------
        RecipeCostReport
            A complete cost report containing:

                - recipe ID
                - recipe name
                - total recipe cost
                - recipe yield quantity
                - recipe yield unit
                - serving size quantity
                - serving size unit
                - cost per yield unit
                - cost per serving
                - individual component cost lines
        
        Raises
        ----------
        ValueError
            Raised if a circular recipe reference is detected.

        --------------------------------------------------------------------------
        RECURSION / VISITED SET
        --------------------------------------------------------------------------

        The 'visited' parameter is one of the most important parts of this method.

        On the initial call:

            visited = None
        
        A new set is then created.

        As each recipe is entered, its ID is added to the set.

        If a component contains another recipe, '_cost_component()' calls 'cost_recipe()' recursively and passed the same set.

        This means a relationship such as:

            Recipe A
                -> Recipe B
                    -> Recipe C

        produces a visited set similar to:

            {A, B, C}

        If Recipe C contains Recipe A, A is already present in the set and the engine knows that a circular reference exists.
        """

        # The initial cller does not need to know about the implementation
        # detail of the visited set, so None means "start a new traversal."
        if visited is None:
            visited = set()

        # Retrivial of Recipe ORM object from repository
        recipe = self.recipe_repo.get(recipe)

        # Checks if current recipe has been encountered in current recursive 
        # chain, if ID is already in visited, the operation is aborted.
        if recipe.id in visited:
            raise ValueError("Circular Recipe Reference")
        
        # Since the circular reference check has passed, we can safely add the 
        # current recipe ID into the visited set
        visited.add(recipe.id)

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

            line = self._cost_component(component, visited)

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
    
    def _cost_component(
            self,
            component,
            visited
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