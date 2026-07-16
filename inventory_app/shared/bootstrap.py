from sqlalchemy.orm import Session

import inventory_app.models
from inventory_app.shared.db import session_scope
from inventory_app.shared.logging import log_operation, get_logger, LogLevels
from inventory_app.common.base import Base
from inventory_app.shared.db import engine
import inventory_app.units.bootstrap as unit
import inventory_app.inventory.bootstrap as inventory
import inventory_app.ingredients.bootstrap as ingredients

logger = get_logger(__name__)


@log_operation(level=LogLevels.INFO)
def seed() -> None:

    with session_scope() as session:
        print("Seeding Units and Unit Categories...")
        unit.seed_defaults(session)

    with session_scope() as session:
        print("Seeding Inventory Locations...")
        inventory.seed_defaults(session)

    with session_scope() as session:
        print("Seeding Ingredient Categories, Subcategories and Ingredients...")
        ingredients.seed_defaults(session)

        print("Bootstrap Complete")



