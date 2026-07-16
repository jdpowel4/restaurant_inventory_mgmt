from sqlalchemy.orm import Session
from typing import Sequence

from inventory_app.vendors.models import VendorItem, VendorItemConversion
from inventory_app.vendors.repositories import conversion_repo

def get_by_item(
        session: Session,
        vendor_item: VendorItem
) -> Sequence[VendorItemConversion]:
    return conversion_repo.get_by_item(session, vendor_item)