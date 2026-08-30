from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Sequence

from inventory_app.recipes.models import Recipe, RecipeComponent
from inventory_app.items.models import Item


class RecipeComponentRepo:

    def __init__(self, session: Session):

        self.session = session

    def get_component(
            self,
            recipe: Recipe,
            item: Item
    ) -> RecipeComponent | None:
        stmt = (select(RecipeComponent)
            .where(
                RecipeComponent.recipe == recipe,
                RecipeComponent.item == item,
            )
        )
        return self.session.scalar(stmt)

    def get_component_by_id(self, id: int) -> RecipeComponent | None:
        return self.session.get(RecipeComponent, id)
            
    def get_by_name(
            self,
            recipe: Recipe,
            item: Item
    ) -> RecipeComponent | None:
        stmt = (select(RecipeComponent)
            .where(
                RecipeComponent.recipe == recipe,
                RecipeComponent.item == item,
            )
        )
        return self.session.scalar(stmt)


    def create(
            self,
            component: RecipeComponent
    ) -> RecipeComponent:

        self.session.add(component)
        return component
    
    def get_components(
            self,
            recipe: Recipe
    ) -> Sequence[RecipeComponent]:
        stmt = select(RecipeComponent).where(RecipeComponent.recipe == recipe)
        return list(self.session.scalars(stmt))