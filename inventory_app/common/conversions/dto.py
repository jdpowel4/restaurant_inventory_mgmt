from dataclasses import dataclass
from decimal import Decimal
from enum import Enum



class ConversionSource(Enum):
    GLOBAL = "global"
    INGREDIENT = "ingredient"
    VENDOR = "vendor"


@dataclass(slots=True)
class ConversionEdge:

    from_unit_id: int
    to_unit_id: int

    multiplier: Decimal

    source: ConversionSource


@dataclass(slots=True)
class ConversionPath:

    edges: list[ConversionEdge]

    multiplier: Decimal