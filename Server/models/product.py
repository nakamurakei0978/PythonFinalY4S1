from . import db
from sqlalchemy import INTEGER, String, ForeignKey, FLOAT
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Product(db.Model):
    id: Mapped[int] = mapped_column(INTEGER, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    image: Mapped[str] = mapped_column(String(255), nullable=True)
    qty: Mapped[int] = mapped_column(INTEGER, default=0)
    price: Mapped[float] = mapped_column(FLOAT, default=0)
    category_id: Mapped[int] = mapped_column(INTEGER, ForeignKey('category.id',ondelete='set null'), nullable=True)
    category = relationship('Category', backref='products', passive_deletes=True)