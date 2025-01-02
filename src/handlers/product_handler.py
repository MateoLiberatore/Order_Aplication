from models.models import Product, db
from app import app 
from sqlalchemy import cast, String

def add_product(name,tag,price,description,stock):
    new_product = Product(
        name=name,
        tag=tag,
        price=price,
        description=description,
        stock=stock
    )
    db.session.add(new_product)
    db.session.commit()
    return new_product

def get_all_products():

    products = Product.query.order_by(Product.id).all()
    detailed_products = [
        {key: getattr(product, key) for key in product.__table__.columns.keys()}
        for product in products
    ]
    return detailed_products
