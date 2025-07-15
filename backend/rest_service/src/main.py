from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
from zeep import Client
import jwt
import datetime
import uuid
from datetime import timezone
from flask import jsonify, request, make_response

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
    token = request.headers.get('Authorization', '')
    print(f"Vérification token : Authorization header = {token}")
    if not token or not token.startswith('Bearer '):
        print("Token manquant ou mal formé")
        return None
    token = token.replace('Bearer ', '')
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        print(f"Payload décodé : {payload}")
        if required_role and payload['role'] not in required_role:
            print(f"Rôle non autorisé : {payload['role']} (requis : {required_role})")
            return None
        return payload
    except jwt.ExpiredSignatureError:
        print("Token expiré")
        return None
    except jwt.InvalidTokenError as e:
        print(f"Token invalide : {str(e)}")
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

from flask import make_response

@app.route('/articles', methods=['GET'])
def get_articles():
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 2))  # ← Ici tu limites bien à 2 par page
        category_id = request.args.get('category_id')
        offset = (page - 1) * per_page

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Total d'articles
        if category_id:
            cursor.execute("SELECT COUNT(*) as total FROM articles WHERE category_id = %s", (category_id,))
        else:
            cursor.execute("SELECT COUNT(*) as total FROM articles")
        total_count = cursor.fetchone()['total']

        # Sélection paginée
        if category_id:
            cursor.execute("SELECT id, title, summary, category_id FROM articles WHERE category_id = %s LIMIT %s OFFSET %s", (category_id, per_page, offset))
        else:
            cursor.execute("SELECT id, title, summary, category_id FROM articles LIMIT %s OFFSET %s", (per_page, offset))

        articles = cursor.fetchall()
        cursor.close()
        conn.close()


        response = make_response(jsonify(articles), 200)
        response.headers['X-Total-Count'] = str(total_count)
        response.headers['Access-Control-Expose-Headers'] = 'X-Total-Count'
        return response
    except Exception as err:
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

@app.route('/categories/<int:id>', methods=['GET'])
def get_category(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, name FROM categories WHERE id = %s", (id,))
        category = cursor.fetchone()
        cursor.close()
        conn.close()
        if category:
            return jsonify(category), 200
        return jsonify({'error': 'Catégorie non trouvée'}), 404
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
        cursor.execute("DELETE FROM articles WHERE category_id = %s", (id,))
        cursor.execute("DELETE FROM categories WHERE id = %s", (id,))
        conn.commit()
        success = cursor.rowcount > 0
        cursor.close()
        conn.close()
        print(f"Suppression catégorie ID {id} et articles associés: {success}")
        return jsonify({'success': success}), 200
    except mysql.connector.Error as err:
        print(f"Erreur MySQL : {err}")
        return jsonify({'error': str(err)}), 500

@app.route('/users', methods=['OPTIONS'])
def users_options():
    return '', 200

@app.route('/users', methods=['GET'])
def get_users():
    payload = verify_token(['administrateur'])
    if not payload:
        print("Échec de la vérification du token")
        return jsonify({'error': 'Accès non autorisé'}), 401
    try:
        client = Client('http://localhost:5001/soap?wsdl')
        users = client.service.listUsers()
        users_serializable = [{'id': user.id, 'username': user.username, 'role': user.role} for user in users]
        print(f"[REST] Utilisateurs récupérés: {len(users_serializable)}")
        print(f"[REST] Données envoyées: {users_serializable}")
        return jsonify(users_serializable), 200
    except Exception as e:
        print(f"Erreur lors de la récupération des utilisateurs : {str(e)}")
        return jsonify({'error': 'Erreur serveur'}), 500

@app.route('/users/<int:id>', methods=['OPTIONS'])
def user_options(id):
    return '', 200

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
        if not all([username, role]):
            return jsonify({'error': 'Champs requis manquants (username, role)'}), 400
        client = Client('http://localhost:5001/soap?wsdl')
        success = client.service.updateUser(id, username, password or '', role)
        return jsonify({'success': success}), 200
    except Exception as e:
        print(f"Erreur lors de la mise à jour de l'utilisateur : {str(e)}")
        return jsonify({'error': f'Erreur serveur: {str(e)}'}), 500

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

@app.route('/tokens', methods=['OPTIONS'])
def tokens_options():
    return '', 200

@app.route('/tokens', methods=['GET'])
def get_tokens():
    payload = verify_token(['administrateur'])
    if not payload:
        return jsonify({'error': 'Accès non autorisé'}), 401
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT token_id, username, role, token, created_at FROM tokens")
        tokens = cursor.fetchall()
        cursor.close()
        conn.close()
        print(f"[REST] Jetons récupérés: {len(tokens)}")
        print(f"[REST] Données envoyées: {tokens}")
        return jsonify(tokens), 200
    except mysql.connector.Error as err:
        print(f"Erreur MySQL : {err}")
        return jsonify({'error': 'Erreur serveur'}), 500

@app.route('/tokens/generate', methods=['POST'])
def generate_token():
    payload = verify_token(['administrateur'])
    if not payload:
        return jsonify({'error': 'Accès non autorisé'}), 401
    data = request.get_json()
    username = data.get('username')
    if not username:
        return jsonify({'error': 'Nom d’utilisateur requis'}), 400
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT username, role FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        if not user:
            cursor.close()
            conn.close()
            return jsonify({'error': 'Utilisateur non trouvé'}), 404
        token_id = str(uuid.uuid4())
        new_token = jwt.encode({
            'username': user['username'],
            'role': user['role'],
            'token_id': token_id,
            'exp': datetime.datetime.now(timezone.utc) + datetime.timedelta(hours=1)
        }, SECRET_KEY, algorithm='HS256')
        cursor.execute(
            "INSERT INTO tokens (token_id, username, role, token, created_at) VALUES (%s, %s, %s, %s, %s)",
            (token_id, user['username'], user['role'], new_token, datetime.datetime.now(timezone.utc))
        )
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Jeton généré pour {username}, token_id: {token_id}")
        return jsonify({'message': 'Jeton généré avec succès', 'token_id': token_id}), 200
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
        print(f"Suppression jeton ID {token_id}: {success}")
        return jsonify({'success': success}), 200
    except mysql.connector.Error as err:
        print(f"Erreur MySQL : {err}")
        return jsonify({'error': 'Erreur serveur'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)