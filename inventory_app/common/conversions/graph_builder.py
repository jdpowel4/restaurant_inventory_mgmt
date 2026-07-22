from sqlalchemy.orm import Session

from inventory_app.common.conversions.graph import ConversionGraph
from inventory_app.common.conversions.dto import ConversionSource
from inventory_app.ingredients.models import Ingredient
from inventory_app.ingredients.services import conversion_service as ingredient_conversion_service
from inventory_app.vendors.models import VendorItem
from inventory_app.vendors.services import conversion_service as vendor_item_conversion_service
from inventory_app.units.models import Unit
from inventory_app.units.services import unit_service

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
        
        units = unit_service.get_all(session)

        by_category: dict[int, list[Unit]] = {}

        for unit in units:
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
        
        conversions = ingredient_conversion_service.get_by_ingredient(session, ingredient)

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
        print("Loading vendor edges")
        conversions = vendor_item_conversion_service.get_by_item(session, vendor_item)

        for conversion in conversions:

            graph.add_bidirectional_edge(
                conversion.from_unit_id,
                conversion.to_unit_id,
                conversion.multiplier,
                ConversionSource.VENDOR
            )