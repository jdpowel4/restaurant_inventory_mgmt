from sqlalchemy.orm import Session

from inventory_app.vendors.models import VendorItem
from inventory_app.vendors.mapping.matcher import MapperMatcher
from inventory_app.vendors.mapping.interactive import InteractiveMapper
from inventory_app.vendors.mapping.dto import MatchResult
from inventory_app.ingredients.interfaces.create import IngredientInterface

def map(
        session: Session,
        item: VendorItem
) -> VendorItem:
    
    interactive = InteractiveMapper()
    interactive.head(item)

    matches = MapperMatcher.find(session, item.vendor_description)

    if not matches:
            print("No Possible Matches Found!")
            return item
     

    selection = interactive.choose_ingredients(matches)
    
    ingredient_interface = IngredientInterface()

    if isinstance(selection, MatchResult):
        item.ingredient = selection.ingredient
        return item
    
    elif selection == "create":        
        ingredient = ingredient_interface.create_from_vend_item(session, item)
        item.ingredient = ingredient
        return item
    
    elif selection == "hint":
        ingredient = ingredient_interface.hint(session)
        item.ingredient = ingredient
        return item

    else:
        raise

