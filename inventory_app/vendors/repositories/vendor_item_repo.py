from sqlalchemy import select
from sqlalchemy.orm import Session

from inventory_app.vendors.models import Vendor, VendorItem

class VendorItemRepo:

        def __init__(self, session: Session):
             
             self.session = session

        def create(
                self,
                item: VendorItem
        ) -> VendorItem:
            self.session.add(item)
            return item


        def get_by_sku(
                self,
                vendor: Vendor,
                sku: str
        ) -> VendorItem | None:
            item = select(VendorItem).where(
                VendorItem.vendor_sku==sku,
                VendorItem.vendor == vendor
        )
            return self.session.scalar(item)

