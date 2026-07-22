from sqlalchemy import select
from sqlalchemy.orm import Session

from inventory_app.vendors.models import Vendor


def get_by_name(
        session: Session,
        name: str
) -> Vendor | None:
    stmt = select(Vendor).where(Vendor.name == name)
    return session.scalar(stmt)

def create(
        session: Session,
        vendor: Vendor
) -> Vendor:
    session.add(vendor)
    return vendor