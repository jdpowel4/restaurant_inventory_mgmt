from sqlalchemy.orm import Session

from inventory_app.shared.logging import get_logger, log_operation, LogLevels
from inventory_app.shared.db import session_scope
from inventory_app.units.services import category_service, unit_service
from inventory_app.units.repositories import category_repo, unit_repo


logger = get_logger(__name__)

@log_operation(level=LogLevels.INFO)
def seed_defaults(
    session: Session,
):

    DEFAULT_CATEGORIES = [
        "Weight",
        "Volume",
        "Count",
        "Case"
    ]

    DEFAULT_UNITS = [

        ("ounce", "oz", "Weight", 1, True),
        ("pound", "lb", "Weight", 16, True),
        ("gram", "g", "Weight", 0.035274, True),
        ("kilogram", "kg", "Weight", 35.274, True),

        ("teaspoon", "tsp", "Volume", 0.1667, True),
        ("tablespoon", "tbsp", "Volume", 0.5, True),
        ("fluid ounce", "floz", "Volume", 1, True),
        ("cup", "c", "Volume", 8, True),
        ("pint", "pt", "Volume", 16, True),
        ("quart", "qt", "Volume", 64, True),
        ("gallon", "gal", "Volume", 128, True),
        ("milliliter", "ml", "Volume", 0.033814, True),
        ("liter", "L", "Volume", 33.814, True),
        
        ("each", "ea", "Count", 1, True),
        ("dozen", "dz", "Count", 12, True),
        ("bottle", "btl", "Count", 1, False),
        ("can", "can", "Count", 1, False),
        ("slice", "slce", "Count", 1, False),
        ("loaf", "loaf", "Count", 1, False),
        ("#10 Can", "#10", "Count", 1, False),
        ("head", "head", "Count", 1, False),
        

        ("case", "cs", "Case", 1, False),
        ("box", "box", "Case", 1, False),
        ("bag", "bag", "Case", 1, False),
        ("sleeve", "slv", "Case", 1, False),
        ("roll", "rl", "Case", 1, False),
        ("bucket", "bkt", "Case", 1, False),
    ]

    categories = {}

    for name in DEFAULT_CATEGORIES:

        categories[name] = category_service.get_or_create(session, name)
    

    for name, abbv, category, factor, allow in DEFAULT_UNITS:


        unit_service.get_or_create(
            session,
            name=name,
            abbv=abbv,
            category=categories[category],
            factor=factor,
            allow=allow
        )
    
    print("Successfully Seeded Unit Categories and Units")

    