from sqlalchemy import select, or_
from sqlalchemy.orm import Session
from typing import Sequence

from inventory_app.inventory.models import *
from inventory_app.purchases.models import Purchase
from inventory_app.recipes.models import Recipe


class InventoryRepo:

    def __init__(
            self,
            session,
    ):
        
        self.session = session

    def create_event(
            self,
            event: InventoryEvent
    ) -> InventoryEvent:
        self.session.add(event)
        return event

    def create_lot(
            self,
            lot: InventoryLot
    ) -> InventoryLot:
        self.session.add(lot)
        return lot

    def create_transaction(
            self,
            transaction: InventoryTransaction
    ) -> InventoryTransaction:
        self.session.add(transaction)
        return transaction
    
    def get_latest_cost_lot(
            self,
            ingredient_id: int
    ) -> InventoryLot:
        return (
            self.session.query(InventoryLot)
            .filter(
                InventoryLot.ingredient_id == ingredient_id
            )
            .order_by(
                InventoryLot.created_at.desc()
            )
            .first()
        )
    