from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Sequence

from inventory_app.purchases.models import Purchase

class PurchaseRepo:

        def __init__(self, session: Session):
             
             self.session = session

        def get(self, id: int) -> Purchase | None:
             return self.session.get(Purchase, id)
        
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
            self.session.commit()
            return purchase

        def get_all(self) -> Sequence[Purchase]:
             stmt = select(Purchase).order_by(Purchase.invoice_date.desc())
             return list(self.session.scalars(stmt))