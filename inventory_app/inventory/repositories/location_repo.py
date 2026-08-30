from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Sequence

from inventory_app.shared.logging import get_logger, LogLevels
from inventory_app.inventory.models import InventoryLocation

logger = get_logger(__name__)

class InventoryLocationRepo:

        def __init__(self, session: Session):
             
             self.session = session

        def get_by_name(
                self,
                name: str
        ) -> InventoryLocation | None:
        
            stmt = select(InventoryLocation).where(InventoryLocation.name == name)

            return self.session.scalar(stmt)

        def create(
                self,
                location: InventoryLocation
        ) -> InventoryLocation:

            self.session.add(location)

            return location
        
        def get_all(self) -> Sequence[InventoryLocation]:
             stmt = select(InventoryLocation).order_by(InventoryLocation.name)
             return list(self.session.scalars(stmt))