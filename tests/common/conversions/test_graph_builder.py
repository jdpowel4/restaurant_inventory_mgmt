from decimal import Decimal
from unittest.mock import patch

from inventory_app.common.conversions.graph_builder import GraphBuilder
from inventory_app.common.conversions.dto import ConversionSource

@patch("inventory_app.common.conversions.graph_builder.unit_service.get_all")
def test_build_empty_graph(mock_units, session):

    mock_units.return_value = []

    graph = GraphBuilder.build(
        session,
        ingredient=None,
        vendor_item=None
    )

    assert graph.neighbors(1) == []

