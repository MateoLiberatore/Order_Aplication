from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()

# Tabla intermedia: relación muchos a muchos entre órdenes y productos
order_products = db.Table(
    'order_products',
    db.Column('order_id', db.Integer, db.ForeignKey('orders.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('products.id'), primary_key=True)
)

# Tabla intermedia: relación muchos a muchos entre órdenes y trabajadores
order_workers = db.Table(
    'order_workers',
    db.Column('order_id', db.Integer, db.ForeignKey('orders.id'), primary_key=True),
    db.Column('worker_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)

class User(db.Model):  # se llama User
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(25), nullable=False)
    direction = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(35), nullable=True)
    dni = db.Column(db.Integer, nullable=False)
    img = db.Column(db.String(255), nullable=True)
    password = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # Por defecto puede ser "client"

    # Un cliente puede tener muchas órdenes
    orders = db.relationship('Order', back_populates='user')

    # Un trabajador puede estar asignado a muchas órdenes (relación muchos a muchos)
    assigned_orders = db.relationship('Order', secondary=order_workers, backref='workers')

    def __repr__(self):
        return (f"<User id={self.id}, name='{self.name}', surname='{self.surname}', "
                f"phone='{self.phone}', direction='{self.direction}', email='{self.email}', "
                f"dni={self.dni}, username='{self.username}', category='{self.category}'>")


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    img = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    tag = db.Column(db.String(25), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(500), nullable=True)
    stock = db.Column(db.Integer, nullable=False)


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now(timezone.utc).replace(microsecond=0))

    # Relación muchos a uno: una orden pertenece a un solo usuario (cliente)
    user = db.relationship('User', back_populates='orders')

    # Relación muchos a muchos con productos
    products = db.relationship('Product', secondary=order_products, backref='orders')
