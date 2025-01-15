from flask import Flask

app = Flask(__name__)

from .clients import client_routes

app.register_blueprint(client_routes.clients_bp) 