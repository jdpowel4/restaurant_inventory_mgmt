from sqlalchemy import select
from sqlalchemy.orm import Session

from inventory_app.vendors.models import VendorItem


def create(
        session: Session,
        item: VendorItem
) -> VendorItem:
    session.add(item)
    return item


def get_by_sku(
        session: Session,
        sku: str
) -> VendorItem | None:
    item = select(VendorItem).where(VendorItem.vendor_sku==sku)
    return session.scalar(item)

