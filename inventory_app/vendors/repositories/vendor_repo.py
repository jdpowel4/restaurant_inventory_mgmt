from sqlalchemy import select
from sqlalchemy.orm import Session

from inventory_app.vendors.models import Vendor

class VendorRepo:

        def __init__(self, session: Session):
             
             self.session = session

        def get_by_name(
                self,
                name: str
        ) -> Vendor | None:
            stmt = select(Vendor).where(Vendor.name == name)
            return self.session.scalar(stmt)

        def create(
                self,
                vendor: Vendor
        ) -> Vendor:
            self.session.add(vendor)
            return vendor