from sqlalchemy.orm import Session
from decimal import Decimal

from inventory_app.purchases.repositories.purchase_item_repo import PurchaseItemRepo
from inventory_app.purchases.models import Purchase, PurchaseItem
from inventory_app.vendors.models import VendorItem

class PurchaseItemService:

    def __init__(self, session: Session):
    
        self.purchase_item_repo = PurchaseItemRepo(session)

    def create(
            self, 
            purchase: Purchase,
            vendor_item: VendorItem,
            quantity: Decimal,
            case_cost: Decimal,
            extended_cost: Decimal
    ) -> PurchaseItem:
        item = PurchaseItem(
            purchase=purchase,
            vendor_item=vendor_item,
            quantity=quantity,
            case_cost=case_cost,
            extended_cost=extended_cost
        )
        return self.purchase_item_repo.create(item)