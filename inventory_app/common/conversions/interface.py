from sqlalchemy.orm import Session
from rich.console import Console
from decimal import Decimal

from inventory_app.common.conversions.exceptions import MissingConversionError
from inventory_app.purchases.models import PurchaseItem
from inventory_app.units.models import Unit
from inventory_app.units.services import unit_service
from inventory_app.ingredients.services import conversion_service as ingredient_conversion_service
from inventory_app.vendors.services import conversion_service as vendor_item_conversion_sercive
from inventory_app.vendors.enum import ConversionSource

class ConversionInterface():

    def __init__(self):
        self.console = Console()
    
    @staticmethod
    def create_conversion(
        session: Session,
        error: MissingConversionError,
        object: PurchaseItem
    ):
        """
        Initalizes CLI Prompt to create vendor_item, or ingredient conversion.
  
        param:
  
        session:
          SQLAlchemy session
        
        error:
          MissingConversionError string

        object: can be any object as long as it has access to a .vendor_item, or .ingredient
        """  

        self = ConversionInterface()
        self.console.print(error)
        self.console.print("Please create a unit conversion for this item.")
        while True:
            conversion_type = self.console.input("Density or Pack? ").strip().lower()

            if conversion_type in ("density", "ingredient"):
                break

            if conversion_type in ("pack", "vendor"):
                break

            self.console.print("[red]Please enter 'density' or 'pack'.[/]")

        from_unit = self._resolve_unit(session, self.console.input("From Unit: "))
        to_unit = self._resolve_unit(session, self.console.input("Please enter To Unit: "))
        multiplier = Decimal(self.console.input("Please enter multiplier: "))

        print(f"ingredient={object.vendor_item.ingredient}")
        print(f"vendor item={object.vendor_item}")
        print(f"from unit={from_unit}")
        print(f"to_unit={to_unit}")
        print(f"multiplier={multiplier}")

        if conversion_type.lower() in ("density", "ingredient"):
            ingredient_conversion_service.create(
                session,
                ingredient=object.vendor_item.ingredient,
                from_unit=from_unit,
                to_unit=to_unit,
                multiplier=multiplier
            )
        
        elif conversion_type.lower() in ("pack", "vendor"):
            user_source: ConversionSource | None = None
            sources = list(ConversionSource)
            self.console.print("[bold]Conversion Sources[/bold]")
            self.console.print()

            for i, source in enumerate(sources, start=1):
                self.console.print(f"{i}. {source.value}")

            while user_source is None:
                try:
                    selection = int(self.console.input("> "))

                    if 1 <= selection <= len(sources):
                        user_source = sources[selection - 1]
                    else:
                        self.console.print("[red]Please choose a valid number.[/]")
                except ValueError:
                    self.console.print("Please make your selection again")


            vendor_item_conversion_sercive.create(
                session,
                item=object.vendor_item,
                from_unit=from_unit,
                to_unit=to_unit,
                multiplier=multiplier,
                source=user_source
            )
    
    def _resolve_unit(
        self,
        session: Session,
        name: Unit | str
    ) -> Unit:
        if isinstance(name, Unit):
            return name
        else:
            return unit_service.get_by_name_or_abbv(session, name)