from argparse import RawDescriptionHelpFormatter
from decimal import Decimal

from inventory_app.shared.db import session_scope
from inventory_app.ingredients.services import ingredient_service, conversion_service
from inventory_app.ingredients.importers import csv_importer

def register_ingredient_commands(subparsers):

    parser = subparsers.add_parser("ingredient")

    ingredient_sub = parser.add_subparsers(dest="ingredient_command")

    add_parser = ingredient_sub.add_parser(
        "create",
        formatter_class=RawDescriptionHelpFormatter,
        description="""
        Creates a new Ingredient.
        
        The ingredient name must be unique.
        Units must already exist.
        Categories must already exist.
        """,
        epilog="""
        Examples:
            inventory ingredient create...
        """)
    
    
    add_parser.add_argument("--name", required=True)
    add_parser.add_argument("--category", required=True)
    add_parser.add_argument("--subcategory", required=True)
    add_parser.add_argument("--base-unit", required=True)
    add_parser.add_argument("--count-unit")
    add_parser.add_argument("--purchase-unit")
    add_parser.add_argument("--location")
    add_parser.set_defaults(func=add_ingredient_command)

    list_parser = ingredient_sub.add_parser("list")
    list_parser.set_defaults(func=list_ingredient_command)

    conversion_parser = ingredient_sub.add_parser("add-conversion")
    conversion_parser.add_argument("ingredient")
    conversion_parser.add_argument("from_unit")
    conversion_parser.add_argument("to_unit")
    conversion_parser.add_argument("multiplier")
    conversion_parser.set_defaults(func=conversion_command)

    import_parser = ingredient_sub.add_parser(
        "import",
        formatter_class=RawDescriptionHelpFormatter,
        description="""
        Imports ingredient list. Must be csv file with headers of 'name', 'category', 'subcategory', 'loaction', 'base_unit', 'count_unit', and 'purchase_unit'
        """
        )
    import_parser.add_argument("file")
    import_parser.set_defaults(func=import_ingredient_command)

    import_conversion = ingredient_sub.add_parser("import_conversion")
    import_conversion.add_arguments("file")
    import_conversion.set_defaults(func=import_conversion_command)


def add_ingredient_command(args):

    with session_scope() as session:

        ingredient_service.create_by_name(
            session,
            name=args.name,
            category=args.category,
            subcategory=args.subcategory,
            base_unit=args.base_unit,
            count_unit=args.count_unit,
            purchase_unit=args.purchase_unit,
            location=args.location
        )


def list_ingredient_command(args):

    with session_scope() as session:

        ingredients = ingredient_service.get_all(session)

        for i in ingredients:

            print(i.item.name)


def conversion_command(args):

    with session_scope() as session:

        conversion_service.create_by_name(
            session,
            ingredient=args.ingredient,
            from_unit=args.from_unit,
            to_unit=args.to_unit,
            multiplier=Decimal(args.multiplier)
        )

def import_ingredient_command(args):

    with session_scope() as session:

        csv_importer.import_ingredient(session, args.file)


def import_conversion_command(args):

    with session_scope() as session:

        csv_importer.import_conversions(session, args.file)