from sqlalchemy.orm import Session

from inventory_app.common.conversions.graph import ConversionGraph
from inventory_app.common.conversions.dto import ConversionSource
from inventory_app.ingredients.models import Ingredient
from inventory_app.ingredients.services.conversion_service import IngredientConversionService
from inventory_app.vendors.models import VendorItem
from inventory_app.vendors.services.conversion_service import VendorItemConversionService
from inventory_app.units.models import Unit
from inventory_app.units.services.unit_service import UnitService

class GraphBuilder:

    def __init__(self):
        pass

    @staticmethod
    def build(
        session: Session,
        ingredient: Ingredient | None,
        vendor_item : VendorItem | None
    ) -> ConversionGraph:
        
        graph = ConversionGraph()

        GraphBuilder._load_global_edges(session, graph)

        if ingredient is not None:
            GraphBuilder._load_ingredient_edges(session, graph, ingredient)

        if vendor_item is not None:
            GraphBuilder._load_vendor_edges(session, graph, vendor_item)
        
        return graph
    
    @classmethod
    def _load_global_edges(
        cls,
        session: Session,
        graph: ConversionGraph
    ) -> None:
        
        unit_service = UnitService(session)

        
        units = unit_service.get_all()

        by_category: dict[int, list[Unit]] = {}

        for unit in units:
            if unit.allow_global_conversions:
                by_category.setdefault(unit.category_id, []).append(unit)
        
        for catrgory_units in by_category.values():

            for from_unit in catrgory_units:

                for to_unit in catrgory_units:

                    if from_unit.id == to_unit.id:
                        continue

                    multiplier = from_unit.factor / to_unit.factor

                    graph.add_bidirectional_edge(
                        from_unit.id,
                        to_unit.id,
                        multiplier,
                        ConversionSource.GLOBAL
                    )

    @classmethod
    def _load_ingredient_edges(
        cls,
        session: Session,
        graph: ConversionGraph,
        ingredient: Ingredient
    ) -> None:
        
        ingredient_conversion_service = IngredientConversionService(session)

        conversions = ingredient_conversion_service.get_by_ingredient(ingredient)

        for conversion in conversions:

            graph.add_bidirectional_edge(
                conversion.from_unit_id,
                conversion.to_unit_id,
                conversion.multiplier,
                ConversionSource.INGREDIENT
            )

    @classmethod
    def _load_vendor_edges(
        cls,
        session: Session,
        graph: ConversionGraph,
        vendor_item: VendorItem
    ) -> None:
        
        vendor_item_conversion_service = VendorItemConversionService(session)

        conversions = vendor_item_conversion_service.get_by_item(vendor_item)

        for conversion in conversions:

            graph.add_bidirectional_edge(
                conversion.from_unit_id,
                conversion.to_unit_id,
                conversion.multiplier,
                ConversionSource.VENDOR
            )