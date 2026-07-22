from inventory_app.purchases.services.normalize_service import *
from inventory_app.purchases.dto import NormalizedInvoice, NormalizedInvoiceLineItem
from inventory_app.purchases.importers.base import BaseImporter, Rows


class USFoodsImporter(BaseImporter):

    vendor_name = "US Foods"

    def parse(
            self,
            rows: Rows
    ) -> NormalizedInvoice:
        
        first = rows[0]

        invoice = NormalizedInvoice(
            vendor_name=self.vendor_name,
            invoice_number=parse_text(first["DocumentNumber"]),
            invoice_date=parse_date(first["DocumentDate"]),
            total=parse_money(first["NetAmountAfter Adjustment"]),
            line_items=[]
        )
        

        for row in rows:

            invoice.line_items.append(
                NormalizedInvoiceLineItem(
                    vendor_sku=parse_text(row["ProductNumber"]),
                    description=parse_text(row["ProductDescription"]),
                    quantity=parse_quantity(row["QtyShip"]),
                    unit=row["PricingUnit"].lower(),
                    unit_price=parse_money(row["UnitPrice"]),
                    extended_price=parse_money(row["ExtendedPrice"]),
                    weight=parse_weight(row["Weight"])
                )
            )
        
        return invoice