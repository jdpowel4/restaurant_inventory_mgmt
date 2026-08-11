from decimal import Decimal

from inventory_app.ingredients.exceptions import NoCostDataError
from inventory_app.inventory.repositories.inventory_repo import InventoryRepo
from inventory_app.vendors.models import VendorItem


class IngredientCostService:

    def __init__(
            self,
            session
    ):
        self.session = session
        self.inventory_repo = InventoryRepo(session)

    
    def get_cost(
            self,
            ingredient_id: int,
            method: str
    ) -> tuple[Decimal, VendorItem, str]:
        
        if method == "most_recent_cost":

            lot = self.inventory_repo.get_latest_cost_lot(
                ingredient_id
            )
            
            if lot is None:
                raise NoCostDataError(ingredient_id)
            return (
                lot.base_unit_cost,
                lot.purchase_item.vendor_item,
                "most_recent_cost"
            )
        
        raise NotImplementedError(method)