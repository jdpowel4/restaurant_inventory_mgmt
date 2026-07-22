from sqlalchemy.orm import Session

from inventory_app.shared.logging import get_logger
from inventory_app.common.enums import EventType
from inventory_app.common.conversions.exceptions import MissingConversionError
from inventory_app.common.conversions.conversion_engine import ConversionEngine
from inventory_app.common.conversions.interface import ConversionInterface
from inventory_app.inventory.models import *
from inventory_app.inventory.repositories import inventory_repo
from inventory_app.purchases.models import Purchase, PurchaseItem
from inventory_app.recipes.models import Recipe
from inventory_app.ingredients.models import Ingredient

logger = get_logger(__name__)


def create_event(
        session: Session,
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
    
    return inventory_repo.create_event(session, event)

def recieve_inventory(
        session: Session,
        event: InventoryEvent,
        purchase_item: PurchaseItem
):
    
    
    while True:
        try:
            quantity = ConversionEngine.convert(
                session=session,
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
                session=session,
                error=e,
                object=purchase_item
            )
            session.flush()
            
    
    unit_cost = ConversionEngine.convert_unit_cost(
        session,
        cost=purchase_item.case_cost,
        from_unit=purchase_item.vendor_item.pack_unit,
        to_unit=purchase_item.vendor_item.ingredient.base_unit,
        ingredient=purchase_item.vendor_item.ingredient,
        vendor_item=purchase_item.vendor_item
    )

    lot = create_lot(
        session,
        event=event,
        ingredient=purchase_item.vendor_item.ingredient,
        purchase_item=purchase_item,
        location=None,
        quantity=quantity,
        base_unit_cost=unit_cost
    )

    create_transaction(
        session,
        event=event,
        ingredient=purchase_item.vendor_item.ingredient,
        lot=lot,
        type="RECIEVE",
        qty=quantity
    )



def create_lot(
        session: Session,
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
    return inventory_repo.create_lot(session, lot)


def create_transaction(
        session: Session,
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
    return inventory_repo.create_transaction(session, transaction)