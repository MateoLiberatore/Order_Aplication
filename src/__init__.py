# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_wtf import FlaskForm



# db = SQLAlchemy()


# def app():

#     app = Flask(__name__)
#     app.config.from_object('config.Config')
#     db.init_app(app)

#     with app.app_context():
#         from .routes import client_routes
#         db.create_all()

#     return app 