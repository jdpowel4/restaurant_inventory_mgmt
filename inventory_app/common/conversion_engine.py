from collections import deque
from decimal import Decimal
from sqlalchemy.orm import Session

from inventory_app.shared.exceptions import ConversionError, MissingIngredientConversion
from inventory_app.units.models import Unit
from inventory_app.ingredients.models import Ingredient
from inventory_app.ingredients.repositories.conversion_repo import get_conversion
from inventory_app.vendors.models import VendorItem


class ConversionEngine:

    """
    Calculates quantity change between different units.

    Conversion hierarchy:

    1. Direct global conversion
    2. Ingredient-specific conversion
    3. Multi-step BFS path search

    Example:
        case -> pound -> ounce
    """
    @staticmethod
    def convert(
        session: Session,
        quantity: Decimal,
        from_unit: Unit,
        to_unit: Unit,
        ingredient: Ingredient | None,
        vendor_item: VendorItem | None
    ) -> Decimal:
        """
        Classic conversion

        Args:

        1. session
        2. quantity - Inital quantity needing to be converted
        3. from_unit - Original unit (e.g. case, box)
        4. to_unit - Goal unit (e.g. pound, each)
        5. ingredient (Not Required) - populate if converting for an ingredient, may require ingredient specific conversions

        Returns:
            quantity
        """

        if from_unit == to_unit:
            return quantity

        quantity = Decimal(str(quantity))
        
        # Try full path with ingredient conversions included
        multiplier = _find_conversion_path(
            session,
            from_unit,
            to_unit,
            ingredient=ingredient
        )

        if multiplier is not None:
            return quantity * multiplier

        # Try again WITHOUT ingredient conversions
        multiplier = _find_conversion_path(
            session,
            from_unit,
            to_unit,
            ingredient=None
        )

        if multiplier is not None:
            return quantity * multiplier

        # Still Nothing -> Raise Error
        if ingredient:
            raise MissingIngredientConversion(
                ingredient.item.name,
                from_unit.name,
                to_unit.name
            )

        raise ConversionError("Conversion Failed")

    @staticmethod
    def convert_unit_cost(
        session: Session,
        unit_cost: Decimal,
        from_unit: Unit,
        to_unit: Unit,
        ingredient: Ingredient | None
    ) -> Decimal:

        multiplier = _find_conversion_path(
            session,
            from_unit,
            to_unit,
            ingredient
        )

        if multiplier is None:
            raise ConversionError(
                f"No conversion path from"
                f"{from_unit.name} to {to_unit.name}"
            )
        
        return unit_cost / multiplier


def _get_neighbors(
        session: Session,
        unit: Unit,
        ingredient: Ingredient | None
    ) -> list[tuple[Unit, Decimal]]:

    neighbors = []

    # Ingredient Specific Conversions
    if ingredient:
        conversions = get_conversion(session, ingredient)

        for conv in conversions:
            
            if conv.from_unit == unit.id:
                neighbors.append((conv.to_unit, Decimal(str(conv.multiplier))))
            
            if conv.to_unit == unit.id:
                neighbors.append((conv.from_unit, Decimal(1) / Decimal(str(conv.multiplier))))
        
    # Global Conversions
    same_category_units = session.query(Unit).filter(
        Unit.category_id == unit.category_id,
        Unit.allow_global_conversions == True
    ).all()

    if not unit.allow_global_conversions:

        same_category_units = []

    for other in same_category_units:
        if other.id == unit.id:
            continue
        
        # Convert Via Factor
        multiplier = Decimal(str(unit.factor)) / Decimal(str(other.factor))
        neighbors.append((other, multiplier))

    return neighbors

def _find_conversion_path(
        session: Session,
        from_unit: Unit,
        to_unit: Unit,
        ingredient: Ingredient | None
    ) -> Decimal | None:

    queue = deque()
    visited = set()

    queue.append((from_unit, Decimal("1"))) # Current_Unit, accumulated_multiplier

    while queue:
        current, multiplier = queue.popleft()

        if current.id == to_unit.id:
            return multiplier
        
        if current.id in visited:
            continue
        
        visited.add(current.id)

        neighbors = _get_neighbors(session, current, ingredient)

       
        for next_unit, step_multiplier in neighbors:
            
            step_multiplier = Decimal(str(step_multiplier))
            queue.append((next_unit, multiplier * step_multiplier))
        
    return None

