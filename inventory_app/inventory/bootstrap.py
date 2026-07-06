from sqlalchemy.orm import Session

from inventory_app.shared.logging import get_logger, log_operation, LogLevels
from inventory_app.shared.db import session_scope

from inventory_app.inventory.services import locations
from inventory_app.inventory.models import *


logger = get_logger(__name__)

@log_operation(level=LogLevels.INFO)
def seed_defaults(
    session: Session
):
    
    DEFUALT_LOCATIONS = [
        "Walk-In Cooler",
        "Walk-In Freezer",
        "Dry Storage",
        "Prep Line",
        "Reach-In Cooler",
        "Reach-In Freezer",
        "Bar",
        "Produce Storage",
        "Chemical Storage"
    ]

    for name in DEFUALT_LOCATIONS:

        locations.get_or_create(session, name)

    print("Successfully seeded Inventory Categories")