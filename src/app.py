from flask import Flask, render_template
from models.models import db
from routes.users.user_routes import users_bp
import sys
from pathlib import Path
from config import Config


sys.path.append(str(Path(__file__).parent.parent))

app = Flask(__name__, template_folder='templates')
app.config.from_object(Config)
db.init_app(app)



app.register_blueprint(users_bp, url_prefix='/users')
#app.register_blueprint(orders_bp, url_prefix='/orders')
#app.register_blueprint(products_bp, url_prefix='/products')

@app.route('/')

def landing():
    return render_template('home.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True,use_reloader=True )