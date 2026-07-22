from rich.console import Console
from InquirerPy import inquirer

from inventory_app.vendors.models import VendorItem
from inventory_app.vendors.mapping.dto import MatchResult

class InteractiveMapper:

    def __init__(self):
        self.console = Console()


    def head(
            self,
            item: VendorItem
    ):
        
        self.console.print("=" * 40)
        self.console.print("[bold]Vendor Item[/bold]")
        self.console.print("=" * 40)
        self.console.print()
        self.console.print(f"Vendor SKU: {item.vendor_sku}")
        self.console.print(f"Description: {item.vendor_description}")
        self.console.print(f"Pack Size: {item.pack_size} {item.pack_unit}")
        self.console.print()


    def choose_ingredients(
            self,
            ingredients: list[MatchResult]
    ) -> MatchResult:

        choices = [
            {
                "name": f"{match.name} ({match.score}%)",
                "value": match
            }
            for match in ingredients
        ]

        choices.extend(
            [
                {
                    "name": "Hint",
                    "value": "hint"
                },
                {
                    "name": "Create New Ingredient",
                    "value": "create"
                }
            ]
        )
        
        return inquirer.select(
            message="Choose an ingredient",
            choices=choices
        ).execute() 