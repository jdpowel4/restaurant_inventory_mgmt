from sqlalchemy import select
from sqlalchemy.orm import Session

from inventory_app.shared.logging import get_logger, LogLevels
from inventory_app.inventory.models import InventoryLocation

logger = get_logger(__name__)

def get_by_name(
        session: Session,
        name: str
) -> InventoryLocation | None:
    
    stmt = select(InventoryLocation).where(InventoryLocation.name == name)

    return session.scalar(stmt)



def create(
        session: Session,
        location: InventoryLocation
) -> InventoryLocation:

    session.add(location)

    return location