from . import db
from sqlalchemy import INTEGER, String
from sqlalchemy.orm import Mapped, mapped_column

class Category(db.Model):
    id: Mapped[int] = mapped_column(INTEGER, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    image: Mapped[str] = mapped_column(String(255), nullable=True)