from sqlalchemy.orm import Session

from inventory_app.shared.logging import get_logger
from inventory_app.common.enums import EventType
from inventory_app.common.conversions.exceptions import MissingConversionError
from inventory_app.common.conversions.conversion_engine import ConversionEngine
from inventory_app.common.conversions.interface import ConversionInterface
from inventory_app.inventory.models import *
from inventory_app.inventory.repositories.inventory_repo import InventoryRepo
from inventory_app.purchases.models import Purchase, PurchaseItem
from inventory_app.recipes.models import Recipe
from inventory_app.ingredients.models import Ingredient

logger = get_logger(__name__)

class InventoryService:

    def __init__(
            self,
            session
    ):
        self.session = session
        self.inventory_repo = InventoryRepo(session)


    def create_event(
            self,
            event_type: EventType,
            reference_type: str | None,
            reference_id: str | None,
            purchase: Purchase | None,
            recipe: Recipe | None,
            notes: str | None
    ) -> InventoryEvent:
        logger.info(
            f"Creating inventory event for purchase: {purchase}"
        )
        event = InventoryEvent(
            event_type=event_type,
            reference_type=reference_type,
            reference_id=reference_id,
            purchase=purchase,
            recipe=recipe,
            notes=notes
        )

        return self.inventory_repo.create_event(event)

    def recieve_inventory(
            self,
            event: InventoryEvent,
            purchase_item: PurchaseItem
    ):


        while True:
            try:
                conversion_engine = ConversionEngine(self.session)
                quantity = conversion_engine.convert(
                    quantity=purchase_item.quantity,
                    from_unit=purchase_item.vendor_item.pack_unit,
                    to_unit=purchase_item.vendor_item.ingredient.base_unit,
                    ingredient=purchase_item.vendor_item.ingredient,
                    vendor_item=purchase_item.vendor_item
                )
                print(f"Multiplier: {quantity}")
                if quantity is not None:
                    break
            except MissingConversionError as e:
                ConversionInterface.create_conversion(
                    self.session,
                    error=e,
                    object=purchase_item
                )
                self.session.flush()


        unit_cost = conversion_engine.convert_unit_cost(
            cost=purchase_item.case_cost,
            from_unit=purchase_item.vendor_item.pack_unit,
            to_unit=purchase_item.vendor_item.ingredient.base_unit,
            ingredient=purchase_item.vendor_item.ingredient,
            vendor_item=purchase_item.vendor_item
        )

        lot = self.create_lot(
            event=event,
            ingredient=purchase_item.vendor_item.ingredient,
            purchase_item=purchase_item,
            location=None,
            quantity=quantity,
            base_unit_cost=unit_cost
        )

        self.create_transaction(
            event=event,
            ingredient=purchase_item.vendor_item.ingredient,
            lot=lot,
            type="RECIEVE",
            qty=quantity
        )



    def create_lot(
            self,
            event: InventoryEvent,
            ingredient: Ingredient,
            purchase_item: PurchaseItem,
            location: InventoryLocation | None,
            quantity: Decimal,
            base_unit_cost: Decimal
    ) -> InventoryLot:
        lot = InventoryLot(
            event=event,
            ingredient=ingredient,
            purchase_item=purchase_item,
            location=location,
            original_qty=quantity,
            remaining_qty=quantity,
            base_unit_cost=base_unit_cost
        )
        return self.inventory_repo.create_lot(lot)


    def create_transaction(
            self,
            event: InventoryEvent,
            ingredient: Ingredient,
            lot: InventoryLot,
            type: str,
            qty: Decimal
    ) -> InventoryTransaction:
        transaction = InventoryTransaction(
            event=event,
            ingredient=ingredient,
            lot=lot,
            transaction_type=type,
            qty_change=qty
        )
        return self.inventory_repo.create_transaction(transaction)