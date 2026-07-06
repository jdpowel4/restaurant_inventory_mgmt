from sqlalchemy import Select
from sqlalchemy.orm import Session

from inventory_app.shared.logging import get_logger, log_operation, LogLevels
from inventory_app.items.models import Item
from inventory_app.items.repositories import item_repo
from inventory_app.common.enums import ItemType

def create(
        session: Session,
        name: str,
        item_type: ItemType
) -> Item:
    
    item = Item(
        name=name,
        item_type=item_type
    )

    return item_repo.create(session, item)