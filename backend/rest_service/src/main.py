from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
from zeep import Client
import jwt
import datetime
import uuid
from datetime import timezone

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:8000", "allow_headers": ["Content-Type", "Authorization"]}})

SECRET_KEY = "wtxLUd69i"

def get_db_connection():
    try:
        return mysql.connector.connect(
            database="projet_al",
            user="root",
            password="wtxLUd69i",
            host="localhost",
            auth_plugin="mysql_native_password"
        )
    except mysql.connector.Error as err:
        print(f"Erreur de connexion MySQL : {err}")
        raise

def verify_token(required_role=None):
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        if required_role and payload['role'] not in required_role:
            return None
        return payload
    except jwt.InvalidTokenError:
        return None

@app.route('/login', methods=['OPTIONS'])
def login_options():
    return '', 200

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        print(f"Tentative de connexion : {username}")

        client = Client('http://localhost:5001/soap?wsdl')
        role = client.service.authenticate(username, password)
        print(f"Résultat SOAP brut : {role}")

        role_mapping = {
            'admin': 'administrateur',
            'editor': 'editeur',
            'visitor': 'visiteur',
            'administrateur': 'administrateur',
            'editeur': 'editeur',
            'visiteur': 'visiteur',
            'none': 'none'
        }
        mapped_role = role_mapping.get(role, 'none')
        print(f"Rôle mappé : {mapped_role}")

        if mapped_role in ['administrateur', 'editeur']:
            token = jwt.encode({
                'username': username,
                'role': mapped_role,
                'token_id': str(uuid.uuid4()),
                'exp': datetime.datetime.now(timezone.utc) + datetime.timedelta(hours=1)
            }, SECRET_KEY, algorithm='HS256')
            conn = get_db_connection()
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "INSERT INTO tokens (token_id, username, role, token) VALUES (%s, %s, %s, %s)",
                    (str(uuid.uuid4()), username, mapped_role, token)
                )
                conn.commit()
            except mysql.connector.Error as err:
                print(f"Erreur lors de l'insertion du jeton : {err}")
                cursor.close()
                conn.close()
                return jsonify({'error': 'Erreur serveur : impossible d’enregistrer le jeton'}), 500
            cursor.close()
            conn.close()
            print(f"Connexion réussie pour {username}, rôle: {mapped_role}, token: {token}")
            return jsonify({'token': token, 'role': mapped_role}), 200
        else:
            print(f"Échec de la connexion pour {username}: rôle invalide ({role})")
            return jsonify({'error': 'Invalid credentials'}), 401
    except Exception as e:
        print(f"Erreur lors de la connexion : {str(e)}")
        return jsonify({'error': f"Erreur serveur : {str(e)}"}), 500

@app.route('/articles', methods=['GET'])
def get_articles():
    try:
        page = int(request.args.get('page', 1))
        category_id = request.args.get('category_id')
        if page < 1:
            page = 1
        per_page = 10
        offset = (page - 1) * per_page
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        if category_id:
            cursor.execute(
                "SELECT id, title, summary, category_id FROM articles WHERE category_id = %s LIMIT %s OFFSET %s",
                (category_id, per_page, offset)
            )
        else:
            cursor.execute("SELECT id, title, summary, category_id FROM articles LIMIT %s OFFSET %s", (per_page, offset))
        articles = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(articles), 200
    except mysql.connector.Error as err:
        print(f"Erreur MySQL : {err}")
        return jsonify({'error': str(err)}), 500

@app.route('/articles/<int:id>', methods=['GET'])
def get_article(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, title, summary, category_id FROM articles WHERE id = %s", (id,))
        article = cursor.fetchone()
        cursor.close()
        conn.close()
        if article:
            return jsonify(article), 200
        return jsonify({'error': 'Article non trouvé'}), 404
    except mysql.connector.Error as err:
        print(f"Erreur MySQL : {err}")
        return jsonify({'error': str(err)}), 500

@app.route('/articles', methods=['POST'])
def add_article():
    payload = verify_token(['administrateur', 'editeur'])
    if not payload:
        return jsonify({'error': 'Accès non autorisé'}), 401
    try:
        data = request.get_json()
        title = data.get('title')
        summary = data.get('summary')
        category_id = data.get('category_id')
        if not all([title, summary, category_id]):
            return jsonify({'error': 'Champs requis manquants'}), 400
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO articles (title, summary, category_id) VALUES (%s, %s, %s)",
            (title, summary, category_id)
        )
        conn.commit()
        article_id = cursor.lastrowid
        cursor.close()
        conn.close()
        print(f"Article ajouté : {title}")
        return jsonify({'id': article_id}), 201
    except mysql.connector.Error as err:
        print(f"Erreur MySQL : {err}")
        return jsonify({'error': str(err)}), 500

@app.route('/articles/<int:id>', methods=['PUT'])
def update_article(id):
    payload = verify_token(['administrateur', 'editeur'])
    if not payload:
        return jsonify({'error': 'Accès non autorisé'}), 401
    try:
        data = request.get_json()
        title = data.get('title')
        summary = data.get('summary')
        category_id = data.get('category_id')
        if not all([title, summary, category_id]):
            return jsonify({'error': 'Champs requis manquants'}), 400
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE articles SET title = %s, summary = %s, category_id = %s WHERE id = %s",
            (title, summary, category_id, id)
        )
        conn.commit()
        success = cursor.rowcount > 0
        cursor.close()
        conn.close()
        print(f"Mise à jour article ID {id}: {success}")
        return jsonify({'success': success}), 200
    except mysql.connector.Error as err:
        print(f"Erreur MySQL : {err}")
        return jsonify({'error': str(err)}), 500

@app.route('/articles/<int:id>', methods=['DELETE'])
def delete_article(id):
    payload = verify_token(['administrateur', 'editeur'])
    if not payload:
        return jsonify({'error': 'Accès non autorisé'}), 401
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM articles WHERE id = %s", (id,))
        conn.commit()
        success = cursor.rowcount > 0
        cursor.close()
        conn.close()
        return jsonify({'success': success}), 200
    except mysql.connector.Error as err:
        print(f"Erreur MySQL : {err}")
        return jsonify({'error': str(err)}), 500

@app.route('/categories', methods=['GET'])
def get_categories():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, name FROM categories")
        categories = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(categories), 200
    except mysql.connector.Error as err:
        print(f"Erreur MySQL : {err}")
        return jsonify({'error': str(err)}), 500

@app.route('/categories', methods=['POST'])
def add_category():
    payload = verify_token(['administrateur', 'editeur'])
    if not payload:
        return jsonify({'error': 'Accès non autorisé'}), 401
    try:
        data = request.get_json()
        name = data.get('name')
        if not name:
            return jsonify({'error': 'Nom de catégorie requis'}), 400
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO categories (name) VALUES (%s)", (name,))
        conn.commit()
        category_id = cursor.lastrowid
        cursor.close()
        conn.close()
        print(f"Catégorie ajoutée : {name}")
        return jsonify({'id': category_id, 'message': 'Catégorie ajoutée'}), 201
    except mysql.connector.Error as err:
        print(f"Erreur MySQL : {err}")
        return jsonify({'error': str(err)}), 500

@app.route('/categories/<int:id>', methods=['PUT'])
def update_category(id):
    payload = verify_token(['administrateur', 'editeur'])
    if not payload:
        return jsonify({'error': 'Accès non autorisé'}), 401
    try:
        data = request.get_json()
        name = data.get('name')
        if not name:
            return jsonify({'error': 'Nom de catégorie requis'}), 400
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE categories SET name = %s WHERE id = %s", (name, id))
        conn.commit()
        success = cursor.rowcount > 0
        cursor.close()
        conn.close()
        print(f"Mise à jour catégorie ID {id}: {success}")
        return jsonify({'success': success}), 200
    except mysql.connector.Error as err:
        print(f"Erreur MySQL : {err}")
        return jsonify({'error': str(err)}), 500

@app.route('/categories/<int:id>', methods=['DELETE'])
def delete_category(id):
    payload = verify_token(['administrateur', 'editeur'])
    if not payload:
        return jsonify({'error': 'Accès non autorisé'}), 401
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM articles WHERE category_id = %s", (id,))
        count = cursor.fetchone()[0]
        if count > 0:
            cursor.close()
            conn.close()
            return jsonify({'error': 'Impossible de supprimer : des articles sont liés à cette catégorie'}), 400
        cursor.execute("DELETE FROM categories WHERE id = %s", (id,))
        conn.commit()
        success = cursor.rowcount > 0
        cursor.close()
        conn.close()
        print(f"Suppression catégorie ID {id}: {success}")
        return jsonify({'success': success}), 200
    except mysql.connector.Error as err:
        print(f"Erreur MySQL : {err}")
        return jsonify({'error': str(err)}), 500

@app.route('/users', methods=['GET'])
def get_users():
    payload = verify_token(['administrateur'])
    if not payload:
        print("Échec de la vérification du token")
        return jsonify({'error': 'Accès non autorisé'}), 401
    try:
        client = Client('http://localhost:5001/soap?wsdl')
        users = client.service.listUsers()
        print(f"[REST] Utilisateurs récupérés: {len(users)}")
        users_serializable = [{'id': user.id, 'username': user.username, 'role': user.role} for user in users]
        print(f"[REST] Données envoyées: {users_serializable}")
        return jsonify(users_serializable), 200
    except Exception as e:
        print(f"Erreur lors de la récupération des utilisateurs : {str(e)}")
        return jsonify({'error': f'Erreur serveur: {str(e)}'}), 500

@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    payload = verify_token(['administrateur'])
    if not payload:
        print("Échec de la vérification du token")
        return jsonify({'error': 'Accès non autorisé'}), 401
    try:
        client = Client('http://localhost:5001/soap?wsdl')
        users = client.service.listUsers()
        user = next((u for u in users if u.id == id), None)
        if user:
            user_serializable = {'id': user.id, 'username': user.username, 'role': user.role}
            print(f"[REST] Utilisateur récupéré: {user_serializable}")
            return jsonify(user_serializable), 200
        return jsonify({'error': 'Utilisateur non trouvé'}), 404
    except Exception as e:
        print(f"Erreur lors de la récupération de l'utilisateur : {str(e)}")
        return jsonify({'error': f'Erreur serveur: {str(e)}'}), 500

@app.route('/users', methods=['POST'])
def add_user():
    payload = verify_token(['administrateur'])
    if not payload:
        return jsonify({'error': 'Accès non autorisé'}), 401
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        role = data.get('role')
        client = Client('http://localhost:5001/soap?wsdl')
        success = client.service.addUser(username, password, role)
        return jsonify({'success': success}), 200
    except Exception as e:
        print(f"Erreur lors de l'ajout de l'utilisateur : {str(e)}")
        return jsonify({'error': 'Erreur serveur'}), 500

@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    payload = verify_token(['administrateur'])
    if not payload:
        return jsonify({'error': 'Accès non autorisé'}), 401
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        role = data.get('role')
        client = Client('http://localhost:5001/soap?wsdl')
        success = client.service.updateUser(id, username, password, role)
        return jsonify({'success': success}), 200
    except Exception as e:
        print(f"Erreur lors de la mise à jour de l'utilisateur : {str(e)}")
        return jsonify({'error': 'Erreur serveur'}), 500

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    payload = verify_token(['administrateur'])
    if not payload:
        return jsonify({'error': 'Accès non autorisé'}), 401
    try:
        client = Client('http://localhost:5001/soap?wsdl')
        success = client.service.deleteUser(id)
        return jsonify({'success': success}), 200
    except Exception as e:
        print(f"Erreur lors de la suppression de l'utilisateur : {str(e)}")
        return jsonify({'error': 'Erreur serveur'}), 500

@app.route('/tokens', methods=['GET'])
def get_tokens():
    payload = verify_token(['administrateur'])
    if not payload:
        return jsonify({'error': 'Accès non autorisé'}), 401
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT token_id, username, role, created_at FROM tokens")
        tokens = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(tokens), 200
    except mysql.connector.Error as err:
        print(f"Erreur MySQL : {err}")
        return jsonify({'error': 'Erreur serveur'}), 500

@app.route('/tokens/<string:token_id>', methods=['DELETE'])
def delete_token(token_id):
    payload = verify_token(['administrateur'])
    if not payload:
        return jsonify({'error': 'Accès non autorisé'}), 401
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tokens WHERE token_id = %s", (token_id,))
        conn.commit()
        success = cursor.rowcount > 0
        cursor.close()
        conn.close()
        return jsonify({'success': success}), 200
    except mysql.connector.Error as err:
        print(f"Erreur MySQL : {err}")
        return jsonify({'error': 'Erreur serveur'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)