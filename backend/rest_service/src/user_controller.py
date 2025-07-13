# rest_service/src/user_controller.py

from flask import Blueprint, request, jsonify
from utils import get_db_connection, verify_token
from zeep import Client

user_bp = Blueprint('user_bp', __name__)

SOAP_WSDL = 'http://localhost:5001/soap?wsdl'

@user_bp.route('/users', methods=['GET'])
def list_users():
    try:
        payload = verify_token(['administrateur'])
        if not payload:
            return jsonify({'error': 'Unauthorized'}), 401

        client = Client(SOAP_WSDL)
        soap_users = client.service.listUsers()
        
        # Convertir les objets SOAP en dictionnaires
        users = []
        if soap_users:
            for soap_user in soap_users:
                user_dict = {
                    'id': soap_user.id,
                    'username': soap_user.username,
                    'role': {'admin': 'administrateur', 'editor': 'editeur', 'visitor': 'visiteur'}.get(soap_user.role, soap_user.role)
                }
                users.append(user_dict)
        
        print(f"[REST] Utilisateurs récupérés: {len(users)}")
        print(f"[REST] Données envoyées: {users}")
        
        return jsonify(users), 200
    except Exception as e:
        print(f"[Erreur REST] list_users : {str(e)}")
        return jsonify({'error': f'Erreur serveur : {str(e)}'}), 500

@user_bp.route('/users', methods=['POST'])
def add_user():
    try:
        payload = verify_token(['administrateur'])
        if not payload:
            return jsonify({'error': 'Unauthorized'}), 401

        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        role = data.get('role')

        if not all([username, password, role]):
            return jsonify({'error': 'Champs requis manquants'}), 400

        soap_role = {'administrateur': 'admin', 'editeur': 'editor', 'visiteur': 'visitor'}.get(role, role)
        client = Client(SOAP_WSDL)
        result = client.service.addUser(username, password, soap_role)
        
        success = result == "true"
        return jsonify({'success': success}), 200 if success else 400
    except Exception as e:
        print(f"[Erreur REST] add_user : {str(e)}")
        return jsonify({'error': str(e)}), 500

@user_bp.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    try:
        payload = verify_token(['administrateur'])
        if not payload:
            return jsonify({'error': 'Unauthorized'}), 401

        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        role = data.get('role')

        if not all([username, password, role]):
            return jsonify({'error': 'Champs requis manquants'}), 400

        soap_role = {'administrateur': 'admin', 'editeur': 'editor', 'visiteur': 'visitor'}.get(role, role)
        client = Client(SOAP_WSDL)
        result = client.service.updateUser(id, username, password, soap_role)
        
        success = result == "true"
        return jsonify({'success': success}), 200 if success else 400
    except Exception as e:
        print(f"[Erreur REST] update_user : {str(e)}")
        return jsonify({'error': str(e)}), 500

@user_bp.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    try:
        payload = verify_token(['administrateur'])
        if not payload:
            return jsonify({'error': 'Unauthorized'}), 401

        client = Client(SOAP_WSDL)
        result = client.service.deleteUser(id)
        
        success = result == "true"
        return jsonify({'success': success}), 200 if success else 400
    except Exception as e:
        print(f"[Erreur REST] delete_user : {str(e)}")
        return jsonify({'error': str(e)}), 500# rest_service/src/user_controller.py

from flask import Blueprint, request, jsonify
from utils import get_db_connection, verify_token
from zeep import Client

user_bp = Blueprint('user_bp', __name__)

SOAP_WSDL = 'http://localhost:5001/soap?wsdl'

@user_bp.route('/users', methods=['GET'])
def list_users():
    try:
        payload = verify_token(['administrateur'])
        if not payload:
            return jsonify({'error': 'Unauthorized'}), 401

        client = Client(SOAP_WSDL)
        soap_users = client.service.listUsers()
        
        # Convertir les objets SOAP en dictionnaires
        users = []
        if soap_users:
            for soap_user in soap_users:
                user_dict = {
                    'id': soap_user.id,
                    'username': soap_user.username,
                    'role': {'admin': 'administrateur', 'editor': 'editeur', 'visitor': 'visiteur'}.get(soap_user.role, soap_user.role)
                }
                users.append(user_dict)
        
        print(f"[REST] Utilisateurs récupérés: {len(users)}")
        print(f"[REST] Données envoyées: {users}")
        
        return jsonify(users), 200
    except Exception as e:
        print(f"[Erreur REST] list_users : {str(e)}")
        return jsonify({'error': f'Erreur serveur : {str(e)}'}), 500

@user_bp.route('/users', methods=['POST'])
def add_user():
    try:
        payload = verify_token(['administrateur'])
        if not payload:
            return jsonify({'error': 'Unauthorized'}), 401

        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        role = data.get('role')

        if not all([username, password, role]):
            return jsonify({'error': 'Champs requis manquants'}), 400

        soap_role = {'administrateur': 'admin', 'editeur': 'editor', 'visiteur': 'visitor'}.get(role, role)
        client = Client(SOAP_WSDL)
        result = client.service.addUser(username, password, soap_role)
        
        success = result == "true"
        return jsonify({'success': success}), 200 if success else 400
    except Exception as e:
        print(f"[Erreur REST] add_user : {str(e)}")
        return jsonify({'error': str(e)}), 500

@user_bp.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    try:
        payload = verify_token(['administrateur'])
        if not payload:
            return jsonify({'error': 'Unauthorized'}), 401

        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        role = data.get('role')

        if not all([username, password, role]):
            return jsonify({'error': 'Champs requis manquants'}), 400

        soap_role = {'administrateur': 'admin', 'editeur': 'editor', 'visiteur': 'visitor'}.get(role, role)
        client = Client(SOAP_WSDL)
        result = client.service.updateUser(id, username, password, soap_role)
        
        success = result == "true"
        return jsonify({'success': success}), 200 if success else 400
    except Exception as e:
        print(f"[Erreur REST] update_user : {str(e)}")
        return jsonify({'error': str(e)}), 500

@user_bp.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    try:
        payload = verify_token(['administrateur'])
        if not payload:
            return jsonify({'error': 'Unauthorized'}), 401

        client = Client(SOAP_WSDL)
        result = client.service.deleteUser(id)
        
        success = result == "true"
        return jsonify({'success': success}), 200 if success else 400
    except Exception as e:
        print(f"[Erreur REST] delete_user : {str(e)}")
        return jsonify({'error': str(e)}), 500