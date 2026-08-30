from contextlib import contextmanager
from collections.abc import Iterator
from sqlalchemy.orm import Session

from inventory_app.shared.db import SessionLocal
from inventory_app.business.services.business_service import BusinessService
from inventory_app.business.providers.business_provider import BusinessProvider
from inventory_app.business.dto import BusinessInfo
from inventory_app.units.services.unit_service import UnitService

class AppContext:

    def __init__(self):
        self.session_factory = SessionLocal
        self.business = self._load_business()

    def _load_business(self) -> BusinessInfo:

        with self.session_factory() as session:
            
            service = BusinessService(session)
            provider = BusinessProvider(service)

            provider.load()

            return provider.business
    
    @contextmanager
    def session_scope(self) -> Iterator[Session]:
        
        with self.session_factory() as session:
            try:
                yield session
                session.commit()
            except Exception:
                session.rollback()
                raise
            finally:
                session.close()

    def load_unit_service(self, session: Session) -> UnitService:
        unit_service = UnitService(session)
        return unit_service