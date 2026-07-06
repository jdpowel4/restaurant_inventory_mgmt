from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from inventory_app.vendors.models import Vendor, VendorItem
    from inventory_app.inventory.models import InventoryLot

from sqlalchemy import ForeignKey, Date, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from decimal import Decimal

from inventory_app.common.base import Base
from inventory_app.common.mixins import TimestampMixin



class Purchase(Base, TimestampMixin):

    __tablename__ = "purchases"

    id: Mapped[int] = mapped_column(primary_key=True)
    vendor_id: Mapped[int] = mapped_column(ForeignKey("vendors.id"))

    invoice_number: Mapped[int] = mapped_column(nullable=False)
    invoice_date: Mapped[date] = mapped_column(Date)
    total: Mapped[Decimal] = mapped_column(Numeric(10,2))


    vendor: Mapped["Vendor"] = relationship(back_populates="purchases")
    items: Mapped[list["PurchaseItem"]] = relationship(back_populates="purchase", cascade="all, delete-orphan", uselist=True)


    def __repr__(self) -> str:
        return f"<Purchase(date={self.invoice_date}, inv number={self.invoice_number})>"
    


class PurchaseItem(Base, TimestampMixin):

    __tablename__ = "purchase_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    purchase_id: Mapped[int] = mapped_column(ForeignKey("purchases.id"))
    vendor_item_id: Mapped[int] = mapped_column(ForeignKey("vendor_items.id"))
    quantity: Mapped[Decimal] = mapped_column(Numeric(10,2), nullable=False)
    case_cost: Mapped[Decimal] = mapped_column(Numeric(10,2), nullable=False)
    extended_cost: Mapped[Decimal] = mapped_column(Numeric(10,2), nullable=False)


    purchase: Mapped["Purchase"] = relationship(back_populates="items")
    vendor_item: Mapped["VendorItem"] = relationship()
    lots: Mapped["InventoryLot"] = relationship(back_populates="purchase_item")