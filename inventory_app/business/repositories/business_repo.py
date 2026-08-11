from sqlalchemy.orm import Session

from inventory_app.business.model import Business

class BusinessRepo:

    def __init__(
            self,
            session: Session
    ):
        self.session = session

    def get(self) -> Business | None:
        return self.session.get(Business, 1)