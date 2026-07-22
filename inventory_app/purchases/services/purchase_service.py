from sqlalchemy.orm import Session
from datetime import date
from decimal import Decimal

from inventory_app.shared.logging import get_logger, log_operation, LogLevels
from inventory_app.purchases.models import Purchase
from inventory_app.purchases.repositories import purchase_repo
from inventory_app.vendors.models import Vendor

logger = get_logger(__name__)


def get_by_inv_numb(
        session: Session,
        number: str,
) -> Purchase | None:
    return purchase_repo.get_by_inv_numb(session, number)


def create(
    session: Session,
    vendor: Vendor,
    invoice_number: str,
    invoice_date: date,
    total: Decimal
) -> Purchase:
    logger.info(
        f"Creating Purchase for invoice: {invoice_number}, total of ${total}"
    )
    purchase = Purchase(
        vendor=vendor,
        invoice_number=invoice_number,
        invoice_date=invoice_date,
        total=total
    )
    return purchase_repo.create(session, purchase)