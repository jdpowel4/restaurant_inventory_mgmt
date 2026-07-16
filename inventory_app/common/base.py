from sqlalchemy.orm import DeclarativeBase
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from inventory_app.inventory.models import InventoryEvent, InventoryLocation, InventoryLot, InventoryTransaction
    from inventory_app.business.model import Business
    from inventory_app.ingredients.models import Ingredient, IngredientCategory, IngredientSubcategory, IngredientUnitConversion
    from inventory_app.items.models import Item
    from inventory_app.purchases.models import Purchase, PurchaseItem
    from inventory_app.recipes.models import Recipe, RecipeComponent, RecipeProduction
    from inventory_app.units.models import Unit, UnitCategory
    from inventory_app.vendors.models import Vendor, VendorItem, VendorItemConversion

class Base(DeclarativeBase):
    pass