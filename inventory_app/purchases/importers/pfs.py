from inventory_app.purchases.dto import NormalizedInvoice, NormalizedInvoiceLineItem
from inventory_app.purchases.services.normalize_service import *
from inventory_app.purchases.importers.base import BaseImporter, Rows
from inventory_app.purchases.importers.csv_reader import CSVReader


class PFSImporter(BaseImporter):

    vendor_name = "PFS"

    def parse(
            self,
            rows: Rows
    ) -> NormalizedInvoice:
        
        first = rows[0]

        invoice = NormalizedInvoice(
            vendor_name=self.vendor_name,
            invoice_number=parse_text(first["Invoice Number"]),
            invoice_date=parse_date(first["Invoice Date"]),
            total=parse_money(first["Invoice Total"]),
            line_items=[]
        )

        for row in rows:

            weight_field = row.get("Weight", "").strip()

            if weight_field:
                quantity, unit = self._parse_weight_field(weight_field)
            else:
                quantity = parse_quantity(row["Qty Shipped"])
                unit = row["UOM"].lower()


            invoice.line_items.append(
                NormalizedInvoiceLineItem(
                    vendor_sku=parse_text(row["Product #"]),
                    description=parse_text(row["Product Description"]),
                    quantity=quantity,
                    unit=unit,
                    unit_price=parse_money(row["Unit Price"]),
                    extended_price=parse_money(row["Ext. Price"])
                )
            )

        return invoice

    def _parse_weight_field(self, value: str) -> tuple[Decimal, str]:

        """
        Parse strings like:
            '87.200/lb'
            '45.5/oz'
            ''
            None
        
        Returns:
            (physical_weight, weight_unit)
        """

        parts = value.split("/", 1)

        if len(parts) != 2:
            raise ValueError(f"Invalid Weight Field: {value}")

        weight = Decimal(parts[0].strip())
        unit = parts[1].strip().lower()

        return weight, unit        