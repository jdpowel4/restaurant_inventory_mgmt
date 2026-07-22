from decimal import Decimal

from inventory_app.shared.logging import get_logger, LogLevels, log_operation
from inventory_app.shared.db import session_scope
from inventory_app.purchases.dto import NormalizedInvoice
from inventory_app.common.enums import EventType
from inventory_app.purchases.models import Purchase
from inventory_app.purchases.services import purchase_service, normalize_service, purchase_item_service
from inventory_app.vendors.services import vendor_item_service, vendor_service
from inventory_app.inventory.services import inventory_service

logger = get_logger(__name__)

@log_operation
def write(data: NormalizedInvoice):

    with session_scope() as session:

        vendor = vendor_service.get_or_create(session, data.vendor_name)

        existing = purchase_service.get_by_inv_numb(session, data.invoice_number)

        if existing:
            print("Duplicate Invoice Detected - skipping write")
            return

        purchase = purchase_service.create(
            session,
            vendor=vendor,
            invoice_number=data.invoice_number,
            invoice_date=data.invoice_date,
            total=data.total
        ) 
        session.flush()

        event = inventory_service.create_event(
            session,
            event_type=EventType.PURCHASE,
            reference_type="invoice",
            reference_id=data.invoice_number,
            purchase=purchase,
            recipe=None,
            notes=None
        )
        session.flush()

        for line in data.line_items:

            if line.weight:
                quantity = line.weight
            else:
                quantity = line.quantity
            if Decimal(str(quantity)) <= 0:
                print(f"Skipping zero-quantity line: {line.description}")
                continue
            
            unit = normalize_service.parse_unit(session, line.unit)

            vendor_item = vendor_item_service.get_or_create(
                session,
                vendor=vendor,
                vendor_sku=line.vendor_sku,
                vendor_description=line.description,
                pack_size=quantity,
                pack_unit=unit,
                most_recent=line.unit_price,
                ingredient=None
            )
            session.flush()

            vendor_item.most_recent_price = line.unit_price

            purchase_item = purchase_item_service.create(
                session,
                purchase=purchase,
                vendor_item=vendor_item,
                quantity=quantity,
                case_cost=line.unit_price,
                extended_cost=line.extended_price
            )
            session.flush()
            
            if not vendor_item.ingredient:

                vendor_item_service.map(session, vendor_item)
            
                inventory_service.recieve_inventory(session, event, purchase_item)

            else:
                inventory_service.recieve_inventory(session, event, purchase_item)

            