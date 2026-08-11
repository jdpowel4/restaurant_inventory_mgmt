from sqlalchemy.orm import Session
from decimal import Decimal

from inventory_app.vendors.models import Vendor, VendorItem
from inventory_app.vendors.repositories.vendor_item_repo import VendorItemRepo
from inventory_app.vendors.mapping import engine
from inventory_app.ingredients.models import Ingredient 
from inventory_app.units.models import Unit


class VendorItemService:

    def __init__(self, session: Session):

        self.session = session
        self.vendor_item_repo = VendorItemRepo(session)

    def get_or_create(
            self,
            vendor: Vendor,
            vendor_sku: str,
            vendor_description: str,
            pack_size: Decimal,
            pack_unit: Unit,
            most_recent: Decimal,
            ingredient: Ingredient | None
    ) -> VendorItem:
        existing = self.vendor_item_repo.get_by_sku(vendor, vendor_sku)

        if existing is not None:
            return existing

        item = VendorItem(
            vendor=vendor,
            ingredient=ingredient,
            vendor_sku=vendor_sku,
            vendor_description=vendor_description,
            pack_size=pack_size,
            pack_unit=pack_unit,
            most_recent_price=most_recent
        )
        return self.vendor_item_repo.create(item)

    def map(
            self,
            vendor_item: VendorItem
    ) -> VendorItem:
        return engine.map(self.session, vendor_item)
