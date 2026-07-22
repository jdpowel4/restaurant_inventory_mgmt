from sqlalchemy.orm import Session
from decimal import Decimal

from inventory_app.purchases.repositories import purchase_item_repo
from inventory_app.purchases.models import Purchase, PurchaseItem
from inventory_app.vendors.models import VendorItem

def create(
        session, 
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
    return purchase_item_repo.create(session, item)