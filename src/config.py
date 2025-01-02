from flask import Flask
from flask_sqlalchemy import SQLAlchemy



class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://admin:admin@localhost:5432/Flask-orders'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

