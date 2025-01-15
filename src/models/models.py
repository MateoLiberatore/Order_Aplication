from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import ARRAY


db = SQLAlchemy()


class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(25), nullable = False)
    surname = db.Column(db.String(50), nullable = False)
    phone = db.Column(db.Integer)
    direction = db.Column(db.String(100), nullable = False)

    #relacion
    orders = db.relationship('Order', back_populates ='client')    #order asociada a un cliente

   
    
class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    tag = db.Column(db.String(25), nullable = False)
    price = db.Column(db.Float, nullable = False)
    description = db.Column(db.String(500), nullable = True)
    stock = db.Column(db.Integer, nullable = False)



class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key= True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.now(timezone.utc).replace(microsecond=0))
    product_id = db.Column(ARRAY(db.Integer), nullable=False) #products ID's
    
    #Relaciones
    client = db.relationship('Client', back_populates='orders')     #cliente asociado a las ordenes


