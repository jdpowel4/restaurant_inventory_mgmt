from sqlalchemy.orm import Session

from inventory_app.shared.logging import get_logger, log_operation, LogLevels
from inventory_app.shared.db import session_scope

from inventory_app.inventory.services import location_service
from inventory_app.inventory.models import *


logger = get_logger(__name__)

@log_operation(level=LogLevels.INFO)
def seed_defaults(
    session: Session
):
    
    DEFUALT_LOCATIONS = [
        "Building",
        "Dish Pit",
        "Dry Stock",
        "Freezer",
        "Wait-Station",
        "Walk-in",
        "3-Door"
    ]

    for name in DEFUALT_LOCATIONS:

        location_service.get_or_create(session, name)

    print("Successfully seeded Inventory Categories")