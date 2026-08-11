from sqlalchemy.orm import Session
from rich.console import Console

from inventory_app.recipes.dto import RecipeCostReport
class RecipeInterface:

    def __init__(self):
        self.console = Console()

    
    def print_recipe_report(
            self,
            report: RecipeCostReport
    ):

        print("=" * 60)
        print("RECIPE COST REPORT")
        print("=" * 60)
        print()
        print(f"Recipe: {report.recipe_name}")
        print(f"Yield: {report.yield_qty:.2f} {report.yield_unit}")
        print(f"Serving Cost: ${report.cost_per_serving:.2f}")
        print()
        print("-" * 60)
        print("COMPONENTS")
        print("-" * 60)

        for line in report.component_lines:

            print()
            print(line.component_name)
            print(f"    Qty: {line.recipe_quantity:.2f} {line.recipe_unit}")
            print(f"    Unit Cost: ${line.recipe_unit_cost:.2f}/{line.recipe_unit}")
            print(f"    Extended Cost: ${line.total_cost:.2f}")
            print(f"    Source: {line.source}")

        print()
        print("-" * 60)
        print("SUMMARY")
        print("-" * 60)
        print(f"Total Batch Cost: ${report.total_cost:.2f}")
        print(f"Cost per Yield Unit: ${report.cost_per_yield_unit:.2f}")
        print(f"Cost per Serving: ${report.cost_per_serving:.2f}")