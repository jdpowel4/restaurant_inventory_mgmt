from decimal import Decimal

from inventory_app.common.conversions.dto import ConversionEdge, ConversionPath, ConversionSource

def test_conversion_edge_stores_values():

    edge = ConversionEdge(
        from_unit_id=1,
        to_unit_id=2,
        multiplier=Decimal("16"),
        source=ConversionSource.GLOBAL
    )

    assert edge.from_unit_id == 1
    assert edge.to_unit_id == 2
    assert edge.multiplier == Decimal("16")
    assert edge.source == ConversionSource.GLOBAL


def test_conversion_path_stores_values():

    edge = ConversionEdge(
        1,
        2,
        Decimal("16"),
        ConversionSource.GLOBAL
    )

    path = ConversionPath(
        edges=[edge],
        multiplier=Decimal("16")
    )

    assert len(path.edges) == 1
    assert path.multiplier == Decimal("16")


def test_empty_conversion_path():

    path = ConversionPath(
        edges=[],
        multiplier=Decimal("1")
    )

    assert path.edges == []
    assert path.multiplier == Decimal("1")


def test_conversion_source_values():

    assert ConversionSource.GLOBAL.value == "global"
    assert ConversionSource.INGREDIENT.value == "ingredient"
    assert ConversionSource.VENDOR.value == "vendor"
    