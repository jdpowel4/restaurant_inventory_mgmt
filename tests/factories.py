from decimal import Decimal

from inventory_app.units.models import Unit

def make_unit(
        name="lb",
        factor="1",
        category=None
):
    
    return Unit(
        name=name,
        factor=Decimal(factor),
        category=category
    )

