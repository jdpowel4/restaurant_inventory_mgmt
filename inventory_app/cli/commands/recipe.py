import argparse
from decimal import Decimal

from inventory_app.shared.db import session_scope
from inventory_app.recipes.services.component_service import RecipeComponentService
from inventory_app.recipes.services.recipe_service import RecipeService
from inventory_app.recipes.engines.costing_engine import CostingEngine
from inventory_app.recipes.interfaces.recipe_interface import RecipeInterface


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
    add_parser.add_argument("--yield-qty", required=True)
    add_parser.add_argument("--yield-unit", required=True)
    add_parser.add_argument("--serving-qty", required=True)
    add_parser.add_argument("--serving-unit", required=True)
    add_parser.set_defaults(func=add_recipe_command)

    
    add_component_parser = recipe_sub.add_parser("add-component")
    add_component_parser.add_argument("recipe")
    add_component_parser.add_argument("item")
    add_component_parser.add_argument("quantity")
    add_component_parser.add_argument("unit")
    add_component_parser.set_defaults(func=add_component_command)

    cost_parser = recipe_sub.add_parser("cost")
    cost_parser.add_argument("recipe")
    cost_parser.set_defaults(func=cost_recipe_command)

    export_parser = recipe_sub.add_parser("export")
    export_parser.add_argument("recipe")
    export_parser.set_defaults(func=export_command)


def add_recipe_command(args):

    with session_scope() as session:

        recipe_service = RecipeService(session)
        recipe_service.create_by_name(
            name=args.name,
            yield_qty=Decimal(args.yield_qty),
            yield_unit=args.yield_unit,
            serving_qty=Decimal(args.serving_qty),
            serving_unit=args.serving_unit
        )


def add_component_command(args):

    with session_scope() as session:
        recipe_service = RecipeService(session)
        recipe = recipe_service.get_by_name(args.recipe)

        component_service = RecipeComponentService(session)
        component_service.create_by_name(
            recipe=recipe,
            item=args.item,
            quantity=Decimal(args.quantity),
            unit=args.unit
        )


def cost_recipe_command(args):

    with session_scope() as session:

        engine = CostingEngine(session)
        interface = RecipeInterface()
        service = RecipeService(session)

        recipe = service.get_by_name(args.recipe)

        report = engine.cost_recipe(recipe)

        interface.print_recipe_report(report)


def export_command(args):

    with session_scope() as session:
        recipe_service = RecipeService(session)
        recipe_service.export_recipe_report(args.recipe)