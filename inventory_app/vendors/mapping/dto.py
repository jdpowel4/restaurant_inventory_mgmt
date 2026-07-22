from dataclasses import dataclass

from inventory_app.ingredients.models import Ingredient


@dataclass
class MatchResult:
    name: str
    ingredient: Ingredient
    score: int