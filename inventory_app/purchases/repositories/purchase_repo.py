from sqlalchemy import select
from sqlalchemy.orm import Session

from inventory_app.purchases.models import Purchase

def get_by_inv_numb(
        session: Session,
        number: str
) -> Purchase | None:
    stmt = select(Purchase).where(Purchase.invoice_number==number)
    return session.scalar(stmt)

def create(
        session: Session,
        purchase: Purchase
) -> Purchase:
    session.add(purchase)
    return purchase