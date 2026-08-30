from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Sequence

from inventory_app.shared.logging import get_logger, log_operation, LogLevels
from inventory_app.items.models import *

logger = get_logger(__name__)

class ItemRepo:

    def __init__(self, session: Session):
        self.session = session

    def create(
            self,
            item: Item
    ) -> Item:

        logger.debug(
            f"Creating Item: {item.name}"
        )
        self.session.add(item)
        return item


    def get_by_name(
            self,
            name: str
    ) -> Item | None:
        stmt = select(Item).where(Item.name == name)
        return self.session.scalar(stmt)
    
    def get(
            self,
            id: int
    ) -> Item | None:
        return self.session.get(Item, id)

    def list(self) -> Sequence[Item]:
        stmt = select(Item).order_by(Item.name)
        return list(self.session.scalars(stmt))