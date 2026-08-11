from sqlalchemy import select
from sqlalchemy.orm import Session

from inventory_app.shared.logging import get_logger, log_operation, LogLevels
from inventory_app.recipes.models import Recipe
from inventory_app.items.models import Item

logger = get_logger(__name__)


class RecipeRepo:

    def __init__(
            self,
            session: Session
    ):
        self.session = session


    def get_by_name(
            self,
            name: str
    ) -> Recipe | None:
        stmt = (select(Recipe)
            .join(Recipe.item)
            .where(Item.name == name))
        return self.session.scalar(stmt)


    def create(
            self,
            recipe: Recipe
    ) -> Recipe:
        self.session.add(recipe)
        return recipe
    
    def get(
        self,
        recipe: int | str
    ) -> Recipe:
        if isinstance(recipe, Recipe):
            return recipe
        elif isinstance(recipe, int):
            stmt = select(Recipe).where(Recipe.id == recipe)
        elif isinstance(recipe, str):
            stmt = (
                select(Recipe)
                .join(Item)
                .where(Item.name == recipe)
            )
        else:
            raise TypeError(
                f"Expected int or str, got {type(recipe).__name__}"
            )
        
        result = self.session.execute(stmt).scalar_one_or_none()

        if result is None:
            raise LookupError(f"Recipe '{recipe}' not found.")

        return result