from sqlalchemy.orm import Session
from decimal import Decimal

from inventory_app.common.conversions.exceptions import MissingConversionError
from inventory_app.units.models import Unit
from inventory_app.units.services.unit_service import UnitService
from inventory_app.ingredients.models import Ingredient
from inventory_app.vendors.models import VendorItem
from inventory_app.common.conversions.graph_builder import GraphBuilder


class ConversionEngine:

    def __init__(
            self,
            session
    ):
        self.session = session


    def convert(
        self,
        quantity: Decimal,
        from_unit: Unit | int,
        to_unit: Unit | int,
        ingredient: Ingredient | None,
        vendor_item: VendorItem | None,
    ) -> Decimal:    
        
        if isinstance(from_unit, int):
            service = UnitService(self.session)
            from_unit = service.get(from_unit)
        if isinstance(to_unit, int):
            service = UnitService(self.session)
            to_unit = service.get(to_unit)

        graph = GraphBuilder.build(
            self.session,
            ingredient,
            vendor_item
        )
        '''
        print("\n=== CONVERSION DEBUG ===")
        print(f"FROM: {from_unit.id} {from_unit.name}")
        print(f"TO:   {to_unit.id} {to_unit.name}")

        for unit_id, edges in graph._graph.items():
            print(f"\nUNIT {unit_id}")
            for edge in edges:
                print(
                    f"  -> {edge.to_unit_id} "
                    f"x {edge.multiplier} "
                    f"source={edge.source}"
                )
        print("========================\n")
        '''
        path = graph.find_path(
            from_unit,
            to_unit,
            ingredient,
            vendor_item
        )

        return quantity * path.multiplier
    

    
    def convert_unit_cost(
        self,
        cost: Decimal,
        from_unit: Unit,
        to_unit: Unit,
        ingredient: Ingredient | None,
        vendor_item: VendorItem | None
    ) -> Decimal:
        
        graph = GraphBuilder.build(
            self.session,
            ingredient,
            vendor_item,
        )

        path = graph.find_path(
            from_unit,
            to_unit
        )

        return cost / path.multiplier