from decimal import Decimal

from inventory_app.shared.logging import get_logger, LogLevels, log_operation
from inventory_app.shared.db import session_scope
from inventory_app.purchases.dto import NormalizedInvoice
from inventory_app.common.enums import EventType
from inventory_app.purchases.models import Purchase
from inventory_app.purchases.services.purchase_service import PurchaseService
from inventory_app.purchases.services import normalize_service
from inventory_app.purchases.services.purchase_item_service import PurchaseItemService
from inventory_app.purchases.exceptions import DuplicatePurchaseError
from inventory_app.vendors.services.vendor_item_service import VendorItemService
from inventory_app.vendors.services.vendor_service import VendorService
from inventory_app.inventory.services.inventory_service import InventoryService

logger = get_logger(__name__)

@log_operation
def write(data: NormalizedInvoice):

    with session_scope() as session:

        inventory_service = InventoryService(session)
        vendor_service = VendorService(session)
        vendor_item_service = VendorItemService(session)
        purchase_service = PurchaseService(session)
        purchase_item_service = PurchaseItemService(session)

        vendor = vendor_service.get_or_create(data.vendor_name)

        existing = purchase_service.get_by_inv_numb(data.invoice_number)

        if existing:
            raise DuplicatePurchaseError

        purchase = purchase_service.create(
            vendor=vendor,
            invoice_number=data.invoice_number,
            invoice_date=data.invoice_date,
            total=data.total
        ) 
        session.flush()

        event = inventory_service.create_event(
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
                purchase=purchase,
                vendor_item=vendor_item,
                quantity=quantity,
                case_cost=line.unit_price,
                extended_cost=line.extended_price
            )
            session.flush()
            
            if not vendor_item.ingredient:

                vendor_item_service.map(vendor_item)
            
                inventory_service.recieve_inventory(event, purchase_item)

            else:
                inventory_service.recieve_inventory(event, purchase_item)

            