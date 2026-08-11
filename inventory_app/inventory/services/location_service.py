from sqlalchemy.orm import Session

from inventory_app.shared.logging import get_logger, log_operation, LogLevels
from inventory_app.inventory.models import InventoryLocation
from inventory_app.inventory.repositories.location_repo import InventoryLocationRepo

logger = get_logger(__name__)


class InventoryLocationService:

    def __init__(self, session: Session):

        self.location_repo = InventoryLocationRepo(session)

    def get_or_create(
            self,
            name: str
    ) -> InventoryLocation:

        existing = self.location_repo.get_by_name(name)

        if existing is not None:
            return existing

        location = InventoryLocation(name=name)

        return self.location_repo.create(location)


    def get_by_name(
            self,
            name: str
    ) -> InventoryLocation | None:
        return self.location_repo.get_by_name(name)