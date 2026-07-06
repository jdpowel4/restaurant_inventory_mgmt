import argparse

from inventory_app.shared.db import session_scope
from inventory_app.ingredients.services import ingredient_service, category_service, subcategory_service, conversion_service
from inventory_app.units.services import unit_service

def register_ingredient_commands(subparsers):

    parser = subparsers.add_parser("ingredient")

    ingredient_sub = parser.add_subparsers(dest="ingredient_command")

    add_parser = ingredient_sub.add_parser("add")
    add_parser.add_argument("name")
    add_parser.add_argument("category")
    add_parser.add_argument("subcategory")
    add_parser.add_argument("base_unit")
    add_parser.set_defaults(func=add_ingredient_command)

    list_parser = ingredient_sub.add_parser("list")
    list_parser.set_defaults(func=list_ingredient_command)

    conversion_parser = ingredient_sub.add_parser("add-conversion")
    conversion_parser.add_argument("ingredient")
    conversion_parser.add_argument("from_unit")
    conversion_parser.add_argument("to_unit")
    conversion_parser.add_argument("multiplier")
    conversion_parser.set_defaults(func=conversion_command)


def add_ingredient_command(args):

    with session_scope() as session:

        cat_obj = category_service.get_by_name(session, args.category)
        if cat_obj is None:
            print(f"Unknown Category '{args.category}'")
            return
        
        sub_obj = subcategory_service.get_by_name(session, args.subcategory)
        if sub_obj is None:
            print(f"Unknown Subcategory '{args.subcategory}'")
            return
        
        unit_obj = unit_service.get_by_name(session, args.base_unit)
        if unit_obj is None:
            print(f"Unknown Unit '{args.base_unit}'")
            return


        ingredient_service.get_or_create(
            session,
            name=args.name,
            category=cat_obj,
            subcategory=sub_obj,
            base_unit=unit_obj
        )


def list_ingredient_command(args):

    with session_scope() as session:

        ingredients = ingredient_service.get_all(session)

        for i in ingredients:

            print(i.item.name)


def conversion_command(args):

    with session_scope() as session:

        ing_obj = ingredient_service.get_by_name(session, args.ingredient)
        if ing_obj is None:
            print(f"Unknown Ingredient '{args.ingredient}'")
            return
        
        from_unit_obj = unit_service.get_by_name(session, args.from_unit)
        if from_unit_obj is None:
            print(f"Unknown Unit '{args.from_unit}'")
            return
        
        to_unit_obj = unit_service.get_by_name(session, args.to_unit)
        if to_unit_obj is None:
            print(f"Unknown Unit '{args.to_unit}'")
            return
        

        conversion_service.create(
            session,
            ing_obj,
            from_unit_obj,
            to_unit_obj,
            int(args.multiplier)
        )

        print("Conversion added successfully")