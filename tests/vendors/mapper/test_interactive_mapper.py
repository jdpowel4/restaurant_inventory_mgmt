import pytest
from dataclasses import dataclass

from inventory_app.vendors.mapping.interactive import InteractiveMapper
from inventory_app.vendors.mapping.dto import MatchResult

@dataclass
class FakeItem:
    name: str


@dataclass
class FakeIngredient:
    item: FakeItem

