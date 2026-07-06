from sqlalchemy.orm import Session

from inventory_app.shared.logging import get_logger, log_operation, LogLevels
from inventory_app.inventory.models import InventoryLocation
from inventory_app.inventory.repositories import locations

logger = get_logger(__name__)

def get_or_create(
        session: Session,
        name: str
) -> InventoryLocation:
    
    existing = locations.get_by_name(session, name)

    if existing is not None:
        return existing

    location = InventoryLocation(name=name)
    
    return locations.create(session, location)