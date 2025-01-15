from flask import Blueprint, jsonify, request, render_template
import src.handlers.db_handler as handler
from src.models.models import Client


clients_bp = Blueprint('clients', __name__,
template_folder='templates',static_folder= 'static',
url_prefix='/clients')


@clients_bp.route('/clients')
def clients():
    return render_template('clients.html')


@clients_bp.route('/get_clients', methods=['GET'])
def get_clients(dic_params = None):

    payload = dic_params or request.args.to_dict()

    if not isinstance(payload, dict):
        return jsonify({'error': 'Invalid parameters'}), 400

    try:
        if not payload:
            clients = handler.get_all(Client)

        else:
            clients = handler.search(Client, payload)

        return render_template('get_clients.html', clients = clients)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@clients_bp.route('/create_client', methods=['GET', 'POST'])
def create_client():

    if request.method == 'POST':
        data = {
            "name": request.form.get('name'),
            "surname": request.form.get('surname'),
            "phone": request.form.get('phone'),
            "direction": request.form.get('direction')
        }

        missing_fields = [key for key, value in data.items() if not value]

        if missing_fields:
            return jsonify({"error": f"Missing fields: {','.join(missing_fields)}"}), 400

        handler.add(Client, data)

        return render_template('clients.html', client=data)

    # If GET request, render the form
    return render_template('create_client.html')
