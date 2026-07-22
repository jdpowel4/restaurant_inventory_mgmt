from pathlib import Path

from inventory_app.purchases.importers.registry import ReaderFactory, ImporterFactory
from inventory_app.purchases.persistence import purchase_writer

def import_purchase(path: Path):

    reader = ReaderFactory.get(path)

    raw = reader.read(path)

    vendor = ImporterFactory.get(raw)

    normal = vendor.parse(raw)

    purchase_writer.write(normal)

    return normal.invoice_number