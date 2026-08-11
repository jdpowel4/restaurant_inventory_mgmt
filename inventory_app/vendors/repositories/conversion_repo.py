from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Sequence

from inventory_app.vendors.models import VendorItem, VendorItemConversion


class VendorItemConversionRepo:

        def __init__(self, session: Session):
             
             self.session = session

        def get_by_item(
                self,
                vendor_item: VendorItem
        ) -> Sequence[VendorItemConversion]:
            stmt = select(VendorItemConversion).where(VendorItemConversion.vendor_item == vendor_item)
            return list(self.session.scalars(stmt))

        def create(
                self,
                conversion: VendorItemConversion
        ) -> VendorItemConversion:
            self.session.add(conversion)
            return conversion