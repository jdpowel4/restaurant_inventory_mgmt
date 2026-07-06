from sqlalchemy.orm import Session

from inventory_app.items.models import *
from inventory_app.ingredients.models import *
from inventory_app.units.models import *
from inventory_app.vendors.models import *
from inventory_app.recipes.models import *
from inventory_app.purchases.models import *
from inventory_app.inventory.models import *
from inventory_app.business.model import *


from inventory_app.shared.db import session_scope
from inventory_app.shared.logging import log_operation, get_logger, LogLevels
from inventory_app.common.base import Base
from inventory_app.shared.db import engine
import inventory_app.units.bootstrap as unit
import inventory_app.inventory.bootstrap as inventory
import inventory_app.ingredients.bootstrap as ingredients

logger = get_logger(__name__)

@log_operation(level=LogLevels.INFO)
def init_db():

    print("Creating database tables...")
    Base.metadata.create_all(engine)
    logger.info(
        "Successfully initialized Database"
    )
    print("Database initialized")



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



