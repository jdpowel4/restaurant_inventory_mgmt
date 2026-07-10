from sqlalchemy import select
from sqlalchemy.orm import Session

from inventory_app.recipes.models import Recipe, RecipeComponent
from inventory_app.items.models import Item


def get_component(
        session: Session,
        recipe: Recipe,
        item: Item
) -> RecipeComponent | None:
    stmt = (select(RecipeComponent)
        .where(
            RecipeComponent.recipe == recipe,
            RecipeComponent.item == item,
        )
    )
    return session.scalar(stmt)


def get_by_name(
        session: Session,
        recipe: str,
        item: str
) -> RecipeComponent | None:
    stmt = (select(RecipeComponent)
        .where(
            RecipeComponent.recipe == recipe,
            RecipeComponent.item == item,
        )
    )
    return session.scalar(stmt)


def create(
        session: Session,
        component: RecipeComponent
) -> RecipeComponent:
    
    session.add(component)
    return component