from enum import Enum

class ConversionSource(str, Enum):
    MANUFACTURER_SPEC = "manufacturer_spec"
    MEASURED = "measured"
    ESTIMATED = "estimated"