from sqlalchemy import select
from sqlalchemy.orm import Session

from inventory_app.purchases.models import Purchase

class PurchaseRepo:

        def __init__(self, session: Session):
             
             self.session = session

        def get_by_inv_numb(
                self,
                number: str
        ) -> Purchase | None:
            stmt = select(Purchase).where(Purchase.invoice_number==number)
            return self.session.scalar(stmt)

        def create(
                self,
                purchase: Purchase
        ) -> Purchase:
            self.session.add(purchase)
            return purchase