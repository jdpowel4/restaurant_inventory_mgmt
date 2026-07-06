import argparse
from inventory_app.cli.commands import bootstrap


def build_parser():

    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers()

    bootstrap.register_bootstrap_commands(subparsers)

    return parser