import argparse
from decimal import Decimal

from inventory_app.shared.db import session_scope
from inventory_app.recipes.services import recipe_service, component_service


def register_recipe_commands(subparsers):

    parser = subparsers.add_parser("recipe")

    recipe_sub = parser.add_subparsers(dest="recipe_command")

    add_parser = recipe_sub.add_parser("add")
    add_parser.add_argument(
        "-n",
        "--name",
        required=True,
        help="Name of the Recipe"
    )
    add_parser.add_argument("--yield-qty")
    add_parser.add_argument("--yield-unit")
    add_parser.add_argument("--serving-qty")
    add_parser.add_argument("--serving-unit")
    add_parser.set_defaults(func=add_recipe_command)

    
    add_component_parser = recipe_sub.add_parser("add-component")
    add_component_parser.add_argument("recipe")
    add_component_parser.add_argument("item-name")
    add_component_parser.add_argument("quantity")
    add_component_parser.add_argument("unit")
    add_component_parser.set_defaults(func=add_component_command)


def add_recipe_command(args):

    with session_scope() as session:

        recipe_service.create_by_name(
            session,
            name=args.name,
            yield_qty=Decimal(args.yield_qty),
            yield_unit=args.yield_unit,
            serving_qty=Decimal(args.serving_qty),
            serving_unit=args.serving_unit
        )


def add_component_command(args):

    with session_scope() as session:

        component_service.create_by_name(
            session=session,
            recipe=args.recipe,
            item=args.item,
            quantity=Decimal(args.quantity),
            unit=args.unit
        )
