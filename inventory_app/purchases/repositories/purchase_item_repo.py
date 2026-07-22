from sqlalchemy import select
from sqlalchemy.orm import Session

from inventory_app.purchases.models import PurchaseItem


def create(
        session: Session,
        purchase_item: PurchaseItem
) -> PurchaseItem:
    session.add(purchase_item)
    return purchase_item