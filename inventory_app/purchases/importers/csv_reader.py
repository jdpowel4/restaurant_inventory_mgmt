import csv
from sqlalchemy.orm import Session
from pathlib import Path
from decimal import Decimal

from inventory_app.shared.logging import get_logger
from inventory_app.purchases.importers.base import *


logger = get_logger(__name__)



class CSVReader(BaseReader):
    
    def read(self, path: Path) -> Rows:
        
        with path.open(newline="", mode="r", encoding="utf-8-sig") as f:

            return list(csv.DictReader(f))
        
    
