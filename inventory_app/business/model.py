from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from inventory_app.common.base import Base


class Business(Base):

    __tablename__ = "business"

    id: Mapped[int] = mapped_column(primary_key=True)
    legal_name: Mapped[str] = mapped_column(String, nullable=False)
    dba_name: Mapped[str] = mapped_column(String, nullable=False)


    phone: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    website: Mapped[str] = mapped_column(String, nullable=False)


    address1: Mapped[str] = mapped_column(String, nullable=False)
    address2: Mapped[str | None] = mapped_column(String, nullable=True)
    city: Mapped[str] = mapped_column(String, nullable=False)
    state: Mapped[str] = mapped_column(String, nullable=False)
    zip_code: Mapped[str] = mapped_column(String, nullable=False)
    country: Mapped[str] = mapped_column(String, nullable=False)


    logo_path: Mapped[str] = mapped_column(String)
    receipt_message: Mapped[str] = mapped_column(Text)

    sales_tax_rate: Mapped[str] = mapped_column(String)

