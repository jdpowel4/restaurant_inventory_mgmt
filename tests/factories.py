from decimal import Decimal

from inventory_app.units.models import Unit, UnitCategory
from inventory_app.ingredients.models import Ingredient
from inventory_app.items.models import Item
from inventory_app.common.enums import ItemType


def make_unit(
        name="lb",
        factor="1",
        category=None
):
    
    return Unit(
        name=name,
        factor=Decimal(factor),
        category=category
    )

def make_ingredient_item(
    name: str
) -> Item:
    return Item(
        name=name,
        item_type=ItemType.INGREDIENT
    )

def make_ingredient(
        name: str
) -> Ingredient:
    item = make_ingredient_item(name)
    return Ingredient(item=item)
