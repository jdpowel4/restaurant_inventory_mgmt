from sqlalchemy import select
from sqlalchemy.orm import Session

from inventory_app.shared.logging import get_logger, log_operation, LogLevels
from inventory_app.items.exceptions import ItemError, UnknownItemError
from inventory_app.items.models import Item
from inventory_app.items.repositories.item_repo import ItemRepo
from inventory_app.common.enums import ItemType


class ItemService:

    def __init__(self, session: Session):
        
        self.item_repo = ItemRepo(session)

    def create(
            self,
            name: str,
            item_type: ItemType
    ) -> Item:

        item = Item(
            name=name,
            item_type=item_type
        )

        return self.item_repo.create(item)


    def get_by_name(
            self,
            name: str
    ) -> Item:
        i = self.item_repo.get_by_name(name)
        if i is None:
            raise UnknownItemError(f"Item '{name}' not found.")
        return i