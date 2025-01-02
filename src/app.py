from flask import Flask
from config import Config
from models.models import db, Client, Order, Product



app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()