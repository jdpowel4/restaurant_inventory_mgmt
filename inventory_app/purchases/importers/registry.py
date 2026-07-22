from pathlib import Path

from inventory_app.purchases.importers.base import BaseReader, Rows, BaseImporter
from inventory_app.purchases.exceptions import UnknownFileTypeError, UnknownVendorError
from inventory_app.purchases.importers.csv_reader import CSVReader
from inventory_app.purchases.importers.usfoods import USFoodsImporter
from inventory_app.purchases.importers.pfs import PFSImporter

class ReaderFactory:

    @staticmethod
    def get(path: Path) -> BaseReader:

        suffix = path.suffix.lower()

        match suffix:

            case ".csv":
                return CSVReader()
        
        raise UnknownFileTypeError()
    
class ImporterFactory:

    @staticmethod
    def get(rows: Rows) -> BaseImporter:

        first = rows[0]

        headers = set(first.keys())

        if {
            'USFSalesRep',
            'DocumentNumber',
            'DocumentDate'
            
        }.issubset(headers):
            
            return USFoodsImporter()

        if {
            "Invoice Date",
            "Invoice Number",
            "Invoice Total"
        }.issubset(headers):
            
            return PFSImporter()
        
        raise UnknownVendorError()