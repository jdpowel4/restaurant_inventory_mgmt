from enum import Enum

class ItemType(str, Enum):
    INGREDIENT = "ingredient"
    RECIPE = "recipe"
    MENU_ITEM = "menu_item"


class EventType(str, Enum):
    PURCHASE = "purchase"
    RECIPE_PRODUCTION = "recipe_production"
    ADJUSTMENT = "adjustment"
    WASTE = "waste"