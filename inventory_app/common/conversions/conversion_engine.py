from sqlalchemy.orm import Session
from decimal import Decimal

from inventory_app.common.conversions.exceptions import MissingConversionError
from inventory_app.units.models import Unit
from inventory_app.ingredients.models import Ingredient
from inventory_app.vendors.models import VendorItem
from inventory_app.common.conversions.graph_builder import GraphBuilder


class ConversionEngine:

    @staticmethod
    def convert(
        session: Session,
        quantity: Decimal,
        from_unit: Unit,
        to_unit: Unit,
        ingredient: Ingredient | None,
        vendor_item: VendorItem | None,
    ) -> Decimal:    
        
        graph = GraphBuilder.build(
            session,
            ingredient,
            vendor_item
        )

        path = graph.find_path(
            from_unit,
            to_unit
        )

        return quantity * path.multiplier
    

    @staticmethod
    def convert_unit_cost(
        session: Session,
        cost: Decimal,
        from_unit: Unit,
        to_unit: Unit,
        ingredient: Ingredient | None,
        vendor_item: VendorItem | None
    ) -> Decimal:
        
        graph = GraphBuilder.build(
            session,
            ingredient,
            vendor_item,
        )

        path = graph.find_path(
            to_unit,
            from_unit
        )

        return cost / path.multiplier