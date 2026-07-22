from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Sequence

from inventory_app.vendors.models import VendorItem, VendorItemConversion

def get_by_item(
        session: Session,
        vendor_item: VendorItem
) -> Sequence[VendorItemConversion]:
    stmt = select(VendorItemConversion).where(VendorItemConversion.vendor_item == vendor_item)
    return list(session.scalars(stmt))

def create(
        session: Session,
        conversion: VendorItemConversion
) -> VendorItemConversion:
    session.add(conversion)
    return conversion