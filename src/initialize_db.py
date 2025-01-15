from models.models import db
from app import app

with app.app_context():
    db.create_all()  # Crea las tablas según el esquema actual
