from dataclasses import dataclass

@dataclass
class IngredientUpdate:

    name: str
    category_id: int
    subcategory_id: int
    location_id: int
    base_unit_id: int
    count_unit_id: int
    purchase_unit_id: int
