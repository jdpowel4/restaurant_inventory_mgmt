from sqlalchemy import select, or_
from sqlalchemy.orm import Session
from typing import Sequence

from inventory_app.inventory.models import *
from inventory_app.purchases.models import Purchase
from inventory_app.recipes.models import Recipe

def get_event_by_purchase_or_recipe(
        session: Session,
        purchase: Purchase | None,
        recipe: Recipe | None
) -> InventoryEvent | None:
    stmt = select(InventoryEvent).where(
        or_(
            InventoryEvent.purchase == purchase,
            InventoryEvent.recipe == recipe
        )
    )
    matches = list(session.scalars(stmt))

    match len(matches):
        case 0:
            raise
        case 1:
            return matches[0]
        case _:
            raise

def create_event(
        session: Session,
        event: InventoryEvent
) -> InventoryEvent:
    session.add(event)
    return event

def create_lot(
        session: Session,
        lot: InventoryLot
) -> InventoryLot:
    session.add(lot)
    return lot

def create_transaction(
        session: Session,
        transaction: InventoryTransaction
) -> InventoryTransaction:
    session.add(transaction)
    return transaction