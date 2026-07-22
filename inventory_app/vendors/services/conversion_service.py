from sqlalchemy.orm import Session
from typing import Sequence
from decimal import Decimal

from inventory_app.shared.logging import get_logger
from inventory_app.vendors.models import VendorItem, VendorItemConversion
from inventory_app.vendors.repositories import conversion_repo
from inventory_app.vendors.enum import ConversionSource
from inventory_app.units.models import Unit

logger = get_logger(__name__)


def get_by_item(
        session: Session,
        vendor_item: VendorItem
) -> Sequence[VendorItemConversion]:
    return conversion_repo.get_by_item(session, vendor_item)

def create(
        session: Session,
        item: VendorItem,
        from_unit: Unit,
        to_unit: Unit,
        multiplier: Decimal,
        source: ConversionSource
) -> VendorItemConversion:
    logger.debug(f"Creating VendorItem Conversion for item '{item}'; between units {from_unit} -> {to_unit}")
    conv = VendorItemConversion(
        vendor_item=item,
        from_unit=from_unit,
        to_unit=to_unit,
        multiplier=multiplier,
        source=source
    )
    return conversion_repo.create(session, conv)