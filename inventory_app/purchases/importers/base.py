from abc import ABC, abstractmethod
from pathlib import Path

from inventory_app.purchases.dto import NormalizedInvoice

type Row = dict[str, str]
type Rows = list[Row]


class BaseReader(ABC):
    """Base class for all vendor importers"""

    vendor_name: str

    @abstractmethod
    def read(
            self,
            path: Path
        ) -> Rows:
        """Read a invoice and return it's rows"""
        raise NotImplementedError
    
class BaseImporter(ABC):

    @abstractmethod
    def parse(
        self,
        rows: Rows
    ) -> NormalizedInvoice:
        raise NotImplementedError