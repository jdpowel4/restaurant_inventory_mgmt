import csv
from sqlalchemy.orm import Session
from pathlib import Path
from decimal import Decimal

from inventory_app.shared.logging import get_logger
from inventory_app.units.services import unit_service
from inventory_app.ingredients.services import ingredient_service, category_service, subcategory_service, conversion_service
from inventory_app.inventory.services import location_service

logger = get_logger(__name__)

def import_ingredient(session: Session, path: Path) -> None:
    
    with path.open(newline="", encoding="utf-8-sig") as f:
        
        reader = csv.DictReader(f)

        line_num = None

        try:
            for line_num, row in enumerate(reader, start=2):

                category = category_service.get_by_name(session, row["category"])
                if category is None:
                    return print(f"Unknown Category '{row["category"]}'")
                subcategory = subcategory_service.get_by_name(session, row["subcategory"])
                if subcategory is None:
                    return print(f"Unknown Subcategory '{row["subcategory"]}")
                base_unit = unit_service.get_by_name(session, row["base_unit"])
                if base_unit is None:
                    return print(f"Unknown Base Unit '{row["base_unit"]}'")
                location = location_service.get_by_name(session, row["location"])
                if location is None:
                    return print(f"Unknown Location '{row["location"]}'")
                count_unit = unit_service.get_by_name(session, row["count_unit"])
                if count_unit is None:
                    return print(f"Unknown Count Unit '{row["count_unit"]}'")
                purchase_unit = unit_service.get_by_name(session, row["purchase_unit"])
                if purchase_unit is None:
                    return print(f"Unknown Purchase Unit '{row["purchase_unit"]}'")
                

                ingredient_service.get_or_create(
                    session,
                    name=row["name"],
                    category=category,
                    subcategory=subcategory,
                    base_unit=base_unit,
                    location=location,
                    count_unit=count_unit,
                    purchase_unit=purchase_unit
                )

        except Exception as e:
            logger.exception(
                "Error importing ingredient on line %s",
                line_num
            )


def import_conversions(session: Session, file: Path) -> None:

    with file.open(newline="", encoding="utf-8-sig") as f:

        reader = csv.DictReader(f)

        line_num = None

        try:

            for line_num, row in enumerate(reader, start=2):
                
                conversion_service.create_by_name(
                    session,
                    ingredient=row["ingredient"],
                    from_unit=row["from_unit"],
                    to_unit=row["to_unit"],
                    multiplier=Decimal(row["multiplier"])
                )
        
        except Exception as e:
            logger.exception(
                "Error importing ingredient conversion on line %s",
                line_num
            )