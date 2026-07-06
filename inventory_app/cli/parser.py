import argparse
from inventory_app.cli.commands import bootstrap, ingredient


def build_parser():

    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers()

    bootstrap.register_bootstrap_commands(subparsers)
    ingredient.register_ingredient_commands(subparsers)

    return parser