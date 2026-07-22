from sqlalchemy.orm import Session

from inventory_app.shared.logging import get_logger, log_operation, LogLevels
from inventory_app.vendors.models import Vendor
from inventory_app.vendors.repositories import vendor_repo

logger = get_logger(__name__)

def get_or_create(
        session: Session,
        name: str
) -> Vendor:
    exists = vendor_repo.get_by_name(session, name)

    if exists is not None:
        return exists
    logger.debug(
        f"Creating '{name}' Vendor"
    )
    vendor = Vendor(name=name)
    return vendor_repo.create(session, vendor)