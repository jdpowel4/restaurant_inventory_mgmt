import pytest
from decimal import Decimal

from inventory_app.common.conversions.dto import ConversionSource
from inventory_app.common.conversions.graph import ConversionGraph
from inventory_app.common.conversions.exceptions import MissingConversionError

def test_empty_graph_has_no_neighbors():

    graph = ConversionGraph()

    assert graph.neighbors(1) == []


def test_add_edge():

    graph = ConversionGraph()

    graph._add_edge(
        1,
        2,
        Decimal("16"),
        ConversionSource.GLOBAL
    )

    neighbors = graph.neighbors(1)

    assert len(neighbors) == 1

    edge = neighbors[0]

    assert edge.from_unit_id == 1
    assert edge.to_unit_id == 2
    assert edge.multiplier == Decimal("16")


def test_bidirectional_edge():

    graph = ConversionGraph()

    graph.add_bidirectional_edge(
        1,
        2,
        Decimal("16"),
        ConversionSource.GLOBAL
    )

    forward = graph.neighbors(1)[0]
    reverse = graph.neighbors(2)[0]

    assert forward.from_unit_id == 1
    assert forward.to_unit_id == 2
    assert forward.multiplier == Decimal("16")
    assert forward.source == ConversionSource.GLOBAL

    assert reverse.from_unit_id == 2
    assert reverse.to_unit_id == 1
    assert reverse.multiplier == Decimal("0.0625")
    assert reverse.source == ConversionSource.GLOBAL


def test_find_path_same_unit():

    graph = ConversionGraph()

    path = graph.find_path(
        5,
        5
    )
    
    assert path.multiplier == Decimal("1")
    assert path.edges == []


def test_find_direct_path():

    graph = ConversionGraph()

    graph.add_bidirectional_edge(
        1,
        2,
        Decimal("16"),
        ConversionSource.GLOBAL
    )

    path = graph.find_path(
        1,
        2
    )

    assert path.multiplier == Decimal("16")
    assert len(path.edges) == 1


def test_find_two_hop_path():

    graph = ConversionGraph()

    graph.add_bidirectional_edge(
        1,
        2,
        Decimal("16"),
        ConversionSource.GLOBAL
    )

    graph.add_bidirectional_edge(
        2,
        3,
        Decimal("2"),
        ConversionSource.GLOBAL
    )

    path = graph.find_path(
        1,
        3
    )

    assert path.multiplier == Decimal("32")
    assert len(path.edges) == 2


def test_three_hop_path():

    graph = ConversionGraph()

    graph.add_bidirectional_edge(
        1,
        2,
        Decimal("16"),
        ConversionSource.GLOBAL
    )

    graph.add_bidirectional_edge(
        2,
        3,
        Decimal("2"),
        ConversionSource.GLOBAL
    )

    graph.add_bidirectional_edge(
        3,
        4,
        Decimal("10"),
        ConversionSource.GLOBAL
    )


def test_missing_path():

    graph = ConversionGraph()

    graph.add_bidirectional_edge(
        1,
        2,
        Decimal("16"),
        ConversionSource.GLOBAL
    )

    with pytest.raises(MissingConversionError):

        graph.find_path(
            1,
            9
        )


def test_cycle_does_not_loop():

    graph = ConversionGraph()

    graph.add_bidirectional_edge(
        1,
        2,
        Decimal("2"),
        ConversionSource.GLOBAL,
    )

    graph.add_bidirectional_edge(
        2,
        3,
        Decimal("2"),
        ConversionSource.GLOBAL,
    )

    graph.add_bidirectional_edge(
        3,
        4,
        Decimal("2"),
        ConversionSource.GLOBAL,
    )

    graph.add_bidirectional_edge(
        4,
        1,
        Decimal("2"),
        ConversionSource.GLOBAL,
    )

    path = graph.find_path(
        1,
        3,
    )

    assert path.multiplier == Decimal("4")


def test_reverse_conversion():

    graph = ConversionGraph()

    graph.add_bidirectional_edge(
        1,
        2,
        Decimal("16"),
        ConversionSource.GLOBAL
    )

    path = graph.find_path(
        2,
        1
    )

    assert path.multiplier == Decimal("0.0625")