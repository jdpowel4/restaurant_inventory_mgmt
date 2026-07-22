from decimal import Decimal
from datetime import datetime, date

from inventory_app.units.services import unit_service
from inventory_app.units.models import Unit

DATE_FORMATS = (
    "%m/%d/%Y",
    "%m/%d/%y"
)

def parse_date(value: str) -> date:

    value = value.strip()

    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            pass
    
    raise ValueError(f"Invalid date: {value}")


def parse_money(value: str) -> Decimal:
    
    value = (
        value.strip()
            .replace("$","")
            .replace(",","")
    )

    return Decimal(value)


def parse_quantity(value: str) -> Decimal:

    value = value.strip().replace(",","")

    return Decimal(value)


def parse_text(value: str) -> str:
    return value.strip()


def parse_unit(session, value: str) -> Unit:
    unit = unit_service.get_by_abbv(session, value.strip().lower())
    return unit


def parse_weight(value: str) -> Decimal:
    return Decimal(value)