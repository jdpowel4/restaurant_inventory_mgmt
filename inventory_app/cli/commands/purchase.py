import argparse
from pathlib import Path

from inventory_app.shared.db import session_scope
from inventory_app.shared.config import INVOICE_DIR
from inventory_app.purchases.services import import_service

def register_invoice_commands(subparsers):

    parser = subparsers.add_parser("purchase")

    invoice_sub = parser.add_subparsers(dest="purchase_command")

    import_parser = invoice_sub.add_parser("import")
    import_parser.add_argument("file")
    import_parser.set_defaults(func=import_purchase_command)


def import_purchase_command(args):

    file = INVOICE_DIR / args.file

    if not file.exists():
        print(f"File not found: {file}")

    invoice_number = import_service.import_purchase(file)

    print(f"Successfully imported invoice {invoice_number}")