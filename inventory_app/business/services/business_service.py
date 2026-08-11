from sqlalchemy.orm import Session

from inventory_app.shared.exceptions import BusinessError
from inventory_app.business.dto import BusinessInfo
from inventory_app.business.repositories.business_repo import BusinessRepo

class BusinessService:

    def __init__(
            self,
            session: Session
    ):
        self.repo = BusinessRepo(session)
    
    def get_business(self) -> BusinessInfo:
        
        business = self.repo.get()

        if business is None:
            raise BusinessError("No business has been configured.")
        
        return BusinessInfo(
            name=business.dba_name,
            logo_path=business.logo_path,
            address=f"{business.address1}. {business.city}, {business.zip_code}",
            phone=business.phone,
            email=business.email
        )