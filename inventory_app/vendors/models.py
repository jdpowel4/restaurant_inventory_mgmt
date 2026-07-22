from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from inventory_app.purchases.models import Purchase
    from inventory_app.units.models import Unit
    from inventory_app.ingredients.models import Ingredient

from sqlalchemy import String, ForeignKey, Numeric, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from decimal import Decimal

from inventory_app.common.base import Base
from inventory_app.common.mixins import TimestampMixin
from inventory_app.vendors.enum import ConversionSource



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
    ingredient_id: Mapped[int | None] = mapped_column(ForeignKey("ingredients.id"), nullable=True)

    vendor_sku: Mapped[str] = mapped_column(String)
    vendor_description: Mapped[str] = mapped_column(String)

    pack_size: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    pack_unit_id: Mapped[int] = mapped_column(ForeignKey("units.id"))

    usable_factor: Mapped[Decimal] = mapped_column(Numeric(10,2), default=1.00)
    
    most_recent_price: Mapped[Decimal] = mapped_column(Numeric(10,2), nullable=False)


    ingredient: Mapped["Ingredient"] = relationship(back_populates="vendor_items")
    pack_unit: Mapped["Unit"] = relationship()
    vendor: Mapped["Vendor"] = relationship(back_populates="vendor_items")
    conversions: Mapped[list["VendorItemConversion"]] = relationship(back_populates="vendor_item")


    def __repr__(self) -> str:
        return f"<VendorItem(name='{self.vendor_description}')>"
    


class VendorItemConversion(Base):

    __tablename__ = "vendor_item_conversions"

    id: Mapped[int] = mapped_column(primary_key=True)
    vendor_item_id: Mapped[int] = mapped_column(ForeignKey("vendor_items.id"))
    from_unit_id: Mapped[int] = mapped_column(ForeignKey("units.id"))
    to_unit_id: Mapped[int] = mapped_column(ForeignKey("units.id"))
    multiplier: Mapped[Decimal] = mapped_column(Numeric(10, 4), nullable=False)
    source: Mapped[ConversionSource] = mapped_column(
        Enum(
            ConversionSource,
            native_enum=False
        ),
        nullable=False
    )
    notes: Mapped[str] = mapped_column(String, nullable=True)

    vendor_item: Mapped["VendorItem"] = relationship(back_populates="conversions")
    from_unit: Mapped["Unit"] = relationship(foreign_keys=[from_unit_id])
    to_unit: Mapped["Unit"] = relationship(foreign_keys=[to_unit_id])


    def __repr__(self) -> str:
        return f"<VendorItemConversion(item='{self.vendor_item.vendor_description}': {self.from_unit.name} -> {self.to_unit.name} multiplier:{self.multiplier})"