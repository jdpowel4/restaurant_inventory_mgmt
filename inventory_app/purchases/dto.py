from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import List


@dataclass
class NormalizedInvoiceLineItem:
    vendor_sku: str
    description: str
    quantity: Decimal
    unit: str
    unit_price: Decimal
    extended_price: Decimal
    weight: Decimal | None = None


@dataclass
class NormalizedInvoice:
    vendor_name: str
    invoice_number: str
    invoice_date: date
    total: Decimal
    line_items: List[NormalizedInvoiceLineItem]