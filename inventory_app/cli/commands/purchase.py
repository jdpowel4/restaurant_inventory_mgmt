import argparse


def register_invoice_commands(subparsers):

    parser = subparsers.add_parser("purchase")

    invoice_sub = parser.add_subparsers(dest="purchase_command")

    import_parser = invoice_sub.add_parser("import")
    import_parser.add_argument("vendor")
    import_parser.add_argument("file")
    import_parser.set_defaults(func=import_purchase_command)


def import_purchase_command(args):

    pass