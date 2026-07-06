import argparse

from inventory_app.shared.db import session_scope
from inventory_app.shared.bootstrap import *

def register_bootstrap_commands(subparsers):

    parser = subparsers.add_parser("bootstrap")

    commands = parser.add_subparsers(dest="bootstrap_command")

    init = commands.add_parser("init-db")
    init.set_defaults(func=init_command)
    units = commands.add_parser("seed")
    units.set_defaults(func=bootstrap_units_command)
    

def init_command(args):

    init_db()



def bootstrap_units_command(args):

    seed()