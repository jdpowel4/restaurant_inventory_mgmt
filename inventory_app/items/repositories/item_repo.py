from sqlalchemy import select
from sqlalchemy.orm import Session

from inventory_app.shared.logging import get_logger, log_operation, LogLevels
from inventory_app.items.models import *

logger = get_logger(__name__)

def create(
        session: Session,
        item: Item
) -> Item:
    
    logger.debug(
        f"Creating Item: {item.name}"
    )
    session.add(item)
    return item
    

def get_by_name(
        session: Session,
        name: str
) -> Item | None:
    stmt = select(Item).where(Item.name == name)
    return session.scalar(stmt)