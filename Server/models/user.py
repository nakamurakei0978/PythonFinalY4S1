from . import db
from sqlalchemy import BOOLEAN, INTEGER, String
from sqlalchemy.orm import Mapped, mapped_column

class User(db.Model):
    id: Mapped[int] = mapped_column(INTEGER, primary_key=True)
    public_id: Mapped[str]=mapped_column(String(50), unique=True)
    username: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    active: Mapped[bool] = mapped_column(BOOLEAN)
    admin: Mapped[bool] = mapped_column(BOOLEAN)