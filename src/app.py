from flask import Flask, render_template
from src.models.models import db
from src.routes.clients.client_routes import clients_bp
import sys
from pathlib import Path
from src.config import Config

sys.path.append(str(Path(__file__).parent.parent))

app = Flask(__name__, template_folder='templates')
app.config.from_object(Config)
db.init_app(app)

#with app.app_context():
    #db.create_all()
app.register_blueprint(clients_bp, url_prefix='/clients')

@app.route('/')
def landing():
    return render_template('home.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True,use_reloader=True )