from sqlalchemy.orm import Session

from inventory_app.business.model import Business
from inventory_app.business.services.business_service import BusinessService
from inventory_app.business.dto import BusinessInfo

class BusinessProvider:

    def __init__(
            self,
            service: BusinessService
    ):
        self._business: BusinessInfo | None = None
        self._service = service

    def load(self) -> None:
        self._business = self._service.get_business()

    @property
    def business(self) -> BusinessInfo:
        if self._business is None:
            raise RuntimeError("Business has not been loaded")
        return self._business
    
    def refresh(self) -> None:
        self._business = self._service.get_business()