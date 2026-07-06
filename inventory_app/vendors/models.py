from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from inventory_app.purchases.models import Purchase
    from inventory_app.units.models import Unit
    from inventory_app.ingredients.models import Ingredient

from sqlalchemy import String, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from decimal import Decimal

from inventory_app.common.base import Base
from inventory_app.common.mixins import TimestampMixin



class Vendor(Base):

    __tablename__ = "vendors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)


    purchases: Mapped[list["Purchase"]] = relationship(back_populates="vendor", uselist=True)
    vendor_items: Mapped[list["VendorItem"]] = relationship(back_populates="vendor", uselist=True)


    def __repr__(self) -> str:
        return f"<Vendor(name='{self.name}')>"
    

    def __str__(self) -> str:
        return self.name
    


class VendorItem(Base, TimestampMixin):

    __tablename__ = "vendor_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    vendor_id: Mapped[int] = mapped_column(ForeignKey("vendors.id"))
    ingredient_id: Mapped[int] = mapped_column(ForeignKey("ingredients.id"))

    vendor_sku: Mapped[str] = mapped_column(String)
    vendor_description: Mapped[str] = mapped_column(String)

    pack_size: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    pack_unit_id: Mapped[int] = mapped_column(ForeignKey("units.id"))

    usable_factor: Mapped[Decimal] = mapped_column(Numeric(10,2), default=1.00)
    
    most_recent_price: Mapped[Decimal] = mapped_column(Numeric(10,2), nullable=False)


    ingredient: Mapped["Ingredient"] = relationship(back_populates="vendor_items")
    pack: Mapped["Unit"] = relationship()
    vendor: Mapped["Vendor"] = relationship(back_populates="vendor_items")


    def __repr__(self) -> str:
        return f"<VendorItem(name='{self.vendor_description}')>"
    