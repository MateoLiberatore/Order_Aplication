from flask import Blueprint, jsonify, request, render_template, Response, redirect, url_for
import handlers.db_handler as handler
from models.models import User


users_bp = Blueprint('users', __name__,
template_folder='templates', static_folder='static', url_prefix='/users')


@users_bp.route('/users')
def users():
    try:
        return render_template('users.html')
    except Exception as e:
        error_msg = f"Server error: {str(e)}"
        print(error_msg)
        return render_template("get_users.html", error=error_msg), 500


@users_bp.route('/search_users', methods=['GET'])
def search_users():
    try:
        query = request.args.get('query', '').strip()
        print(f"Query received: {query}")

        if query.lower() == "all":
            results = handler.get_all(User)
            print("RESULTS GET ALL:", results)

            if isinstance(results, dict) and "error" in results:
                return render_template("get_users.html", error=results["error"])
            
            return render_template("get_users.html", users=results)

        elif query:
            dic_params = {
                'name': query,
                'surname': query,
                'email': query,
                'direction': query,
                'dni': query,
                'username': query,
                'category': query,
                'phone': query
            }
            print("dicc: ", dic_params)
            results, status_code = handler.search(User, dic_params)
            if status_code == 200:
                return render_template('get_users.html', success=results), 200
            else:
                return render_template("get_users.html", error=results.get("error")), 500

        else:
            return render_template('get_users.html')

    except Exception as e:
        error_msg = f"Server error: {str(e)}"
        print(error_msg)
        return render_template("get_users.html", error=error_msg), 500


@users_bp.route('/create_users', methods=['GET', 'POST'])
def create_users():
    try:
        if request.method == 'GET':
            return render_template("create_users.html")

        elif request.method == 'POST':
            data = request.form.to_dict()
            print(data)

            if not data:
                return render_template("create_users.html", error={"error": "No data received"}), 400

            missing_fields = [key for key in ["name", "surname", "phone", "direction"] if key not in data or not data[key]]
            if missing_fields:
                errors = {field: "Field is required" for field in missing_fields}
                return render_template("create_users.html", error={"error": errors}), 400

            message, status_code = handler.add(User, data)
            return render_template("create_users.html", success=message), status_code

    except Exception as e:
        response = {"error": f"Server error: {str(e)}"}
        return render_template("create_users.html", error=response), 500


@users_bp.route('/delete_user/<int:id>', methods=['POST'])
def delete_users(id):
    try:
        if request.form.get('_method') == 'DELETE':
            handler.delete(User, {'id':id})
            response = {"success": "User deleted successfully"}
            return render_template('get_users.html', success=response), 200
        else:
            return render_template('get_users.html', error={"error": "Invalid method"}), 405

    except Exception as e:
        response = {"error": f"Could not delete user: {str(e)}"}
        return render_template('get_users.html', error=response), 500


@users_bp.route('/modify_users/<int:id>', methods=['GET', 'POST'])
def modify_users(id):
    try:
        if request.method == 'GET':
            data, status_code = handler.search(User, {'id': id})
            if not data:
                return render_template('get_users.html', error={"error": "User not found"}), 404
            return render_template('modify_users.html', data=data), 200

        elif request.method == 'POST':
            form_data = request.form.to_dict()

            if not form_data:
                return render_template('modify_users.html', error={"error": "No data received"}), 400

            missing_fields = [key for key in ["name", "surname", "phone", "direction"] if key not in form_data or not form_data[key]]
            if missing_fields:
                response = {"error": f"Missing required fields: {', '.join(missing_fields)}"}
                return render_template('modify_users.html', data=form_data, error=response), 400

            field_type_map = {
                'phone': str,
                'name': str,
                'surname': str,
                'directions': str,
            }

            for key, value in form_data.items():
                if key in field_type_map:
                    target_type = field_type_map[key]
                    try:
                        if target_type == str:
                            form_data[key] = str(value)
                        else:
                            form_data[key] = target_type(value)
                    except ValueError:
                        return render_template('modify_users.html', data=form_data, error={"error": f"Invalid data for field '{key}'"}), 400

            response, status_code = handler.modify(User, id, form_data)
            updated_user = handler.search(User, {'id': id})
            return render_template('modify_users.html', data=updated_user, success=response), status_code

    except Exception as e:
        user_data, _ = handler.search(User, {'id': id})
        user = user_data if user_data else {}
        response = {"error": f"Error processing request: {str(e)}"}
        return render_template("modify_users.html", data=user, exception=response), 500
