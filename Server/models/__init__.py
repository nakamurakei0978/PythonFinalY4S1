from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from models.category import Category
from models.product import Product
from models.user import User
from models.sale import Sale
from models.sale_details import Sale_details