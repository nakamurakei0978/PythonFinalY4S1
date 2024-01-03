from . import db
from sqlalchemy import BOOLEAN, INTEGER, String, Date, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

class Sale_details(db.Model):
    id: Mapped[int] = mapped_column(INTEGER, primary_key=True)
    sale_id: Mapped[int]=mapped_column(INTEGER, ForeignKey('sale.id'), nullable=True)
    product_id: Mapped[int]=mapped_column(INTEGER, ForeignKey('product.id'), nullable=True)
    qty: Mapped[int] = mapped_column(INTEGER, default=0)
    price: Mapped[float] = mapped_column(Float, default=0)