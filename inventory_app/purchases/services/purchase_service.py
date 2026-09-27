from sqlalchemy.orm import Session
from datetime import date
from decimal import Decimal
from typing import Sequence

from inventory_app.shared.logging import get_logger, log_operation, LogLevels
from inventory_app.purchases.models import Purchase
from inventory_app.purchases.exceptions import PurchaseError
from inventory_app.purchases.repositories.purchase_repo import PurchaseRepo
from inventory_app.vendors.models import Vendor

logger = get_logger(__name__)


class PurchaseService:

    def __init__(self, session: Session):

        self.purchase_repo = PurchaseRepo(session)

    def get(self, id: int) -> Purchase:
        purchase = self.purchase_repo.get(id)
        if purchase is None:
            raise PurchaseError
        return purchase

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
        try:
            purchase = Purchase(
                vendor=vendor,
                invoice_number=invoice_number,
                invoice_date=invoice_date,
                total=total
            )
            return self.purchase_repo.create(purchase)
        
        except Exception:
            raise PurchaseError("Could Not Save Purchase")

    def get_all(self) -> Sequence[Purchase]:
        return self.purchase_repo.get_all()