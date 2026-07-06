from decimal import Decimal
from sqlalchemy import String, ForeignKey, Numeric, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column

from inventory_app.common.base import Base



class UnitCategory(Base):

    __tablename__ = "unit_categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    

    units: Mapped[list["Unit"]] = relationship(back_populates="category")


    def __repr__(self):
        return f"<UnitCategory(name='{self.name}')>"
    
    def __str__(self): # type: ignore
        return self.name
    


class Unit(Base):

    __tablename__ = "units"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    abbreviation: Mapped[str | None] = mapped_column(String, nullable=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("unit_categories.id"))
    factor: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    allow_global_conversions: Mapped[bool] = mapped_column(Boolean, default=True)
    

    category: Mapped["UnitCategory"] = relationship(back_populates="units")


    def __repr__(self) -> str:
        return f"<Unit(name='{self.name}')>"
    
    def __str__(self) -> str:
        return self.name