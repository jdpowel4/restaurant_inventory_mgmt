from inventory_app.purchases.services.normalize_service import *
from inventory_app.purchases.dto import NormalizedInvoice, NormalizedInvoiceLineItem
from inventory_app.purchases.importers.base import BaseImporter, Rows


class WestwaterHams(BaseImporter):

    vendor_name = "Westwater Country Hams"

    def parse(
        self,
        rows: Rows
    ) -> NormalizedInvoice:
        
        first = rows[0]

        invoice = NormalizedInvoice(
            vendor_name=self.vendor_name,
            invoice_number=parse_text(first["invoice_number"]),
            invoice_date=parse_date(first["date"]),
            total=parse_money(first["total"]),
            line_items=[]
        )

        for row in rows:

            invoice.line_items.append(
                NormalizedInvoiceLineItem(
                    vendor_sku=parse_text(row["sku"]),
                    description=parse_text(row["name"]),
                    quantity=parse_quantity(row["quantity"]),
                    unit=row["unit"].lower(),
                    unit_price=parse_money(row["unit_cost"]),
                    extended_price=parse_money(row["extended_price"]),
                    weight=parse_weight(row["weight"])
                )
            )

        return invoice