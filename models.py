from extensions import db
from sqlalchemy import Numeric

class ProductCategories(db.Model):
    __tablename__ = "product_categories"
    
    category_id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False)
    img_url = db.Column(db.String(200), nullable=False)
    products = db.relationship("Products", backref="category")

class Products(db.Model):
    _tablename__ = "products"

    product_id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False)
    img_url = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Numeric(10,2), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("product_categories.category_id"), nullable=False)