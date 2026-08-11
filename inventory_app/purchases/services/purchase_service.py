from sqlalchemy.orm import Session
from datetime import date
from decimal import Decimal

from inventory_app.shared.logging import get_logger, log_operation, LogLevels
from inventory_app.purchases.models import Purchase
from inventory_app.purchases.repositories.purchase_repo import PurchaseRepo
from inventory_app.vendors.models import Vendor

logger = get_logger(__name__)


class PurchaseService:

    def __init__(self, session: Session):

        self.purchase_repo = PurchaseRepo(session)

    def get_by_inv_numb(
            self,
            number: str,
    ) -> Purchase | None:
        return self.purchase_repo.get_by_inv_numb(number)


    def create(
        self,
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
        return self.purchase_repo.create(purchase)