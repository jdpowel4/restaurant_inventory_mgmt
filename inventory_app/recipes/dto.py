from dataclasses import dataclass
from decimal import Decimal
from typing import List
from datetime import datetime


@dataclass
class ComponentCostLine:
    component_id: int
    component_name: str
    recipe_quantity: Decimal
    recipe_unit: str
    recipe_unit_cost: Decimal
    total_cost: Decimal
    source: str 

@dataclass
class RecipeCostReport:
    recipe_id: int | None
    recipe_name: str
    total_cost: Decimal
    yield_qty: Decimal
    yield_unit: str
    serving_qty: Decimal
    serving_unit: str
    num_of_servings: Decimal
    cost_per_yield_unit: Decimal
    cost_per_serving: Decimal
    component_lines: List[ComponentCostLine]

@dataclass
class ReportMetadata:
    title: str
    author: str
    subject: str
    created: datetime
    company_name: str
    filename: str

@dataclass
class RecipeComponentInput:
    id: int | None
    quantity: Decimal
    unit_id: int
    item_id: int
    pre_instructions: str = ""
    post_instructions: str = ""

@dataclass
class RecipeInput:
    recipe_id: int | None
    recipe_name: str
    yield_qty: Decimal
    yield_unit_id: int
    serving_qty: Decimal
    serving_unit_id: int
    components: List[RecipeComponentInput]