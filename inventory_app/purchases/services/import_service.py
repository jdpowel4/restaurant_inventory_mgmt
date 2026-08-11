from pathlib import Path

from inventory_app.purchases.importers.registry import ReaderFactory, ImporterFactory
from inventory_app.purchases.exceptions import DuplicatePurchaseError
from inventory_app.purchases.persistence import purchase_writer

def import_purchase(path: Path):

    reader = ReaderFactory.get(path)

    raw = reader.read(path)

    vendor = ImporterFactory.get(raw)

    normal = vendor.parse(raw)

    purchase_writer.write(normal)

    return normal.invoice_number


def import_directory(path: Path):

    imported = 0
    failed = 0

    for file in sorted(path.rglob("*")):
        if not file.is_file():
            continue

        try:
            import_purchase(file)
            imported += 1

        except DuplicatePurchaseError:
            print(f"Skipping duplicate {file.name}")
        
        except Exception as e:
            failed += 1
            print(f"{file.name}: {e}")
        
    return imported, failed