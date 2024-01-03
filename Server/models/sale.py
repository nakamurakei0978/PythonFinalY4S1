from . import db
from sqlalchemy import BOOLEAN, INTEGER, String, Date, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

class Sale(db.Model):
    id: Mapped[int] = mapped_column(INTEGER, primary_key=True)
    user_id: Mapped[int]=mapped_column(INTEGER, ForeignKey('user.id'), nullable=True)
    sale_date: Mapped[Date] = mapped_column(Date)
    total_amount: Mapped[float] = mapped_column(Float)
    