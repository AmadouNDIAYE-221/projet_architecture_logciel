# backend/rest_service/src/main.py
#password="wtxLUd69i",  # Remplacez par votre mot de passe
from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
from zeep import Client

app = Flask(__name__)
CORS(app)

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

@app.route('/articles', methods=['GET'])
def get_articles():
    try:
        page = int(request.args.get('page', 1))
        category = request.args.get('category', None)
        if page < 1:
            page = 1
        per_page = 10
        offset = (page - 1) * per_page
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        if category:
            cursor.execute(
                "SELECT id, title, summary, category_id FROM articles WHERE category_id = %s LIMIT %s OFFSET %s",
                (category, per_page, offset)
            )
        else:
            cursor.execute("SELECT id, title, summary, category_id FROM articles LIMIT %s OFFSET %s", (per_page, offset))
        articles = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(articles)
    except mysql.connector.Error as err:
        print(f"Erreur MySQL : {err}")
        return jsonify({"error": str(err)}), 500
    except ValueError as err:
        print(f"Erreur de valeur : {err}")
        return jsonify({"error": "Invalid page or category parameter"}), 400

@app.route('/categories', methods=['GET'])
def get_categories():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, name FROM categories")
        categories = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(categories)
    except mysql.connector.Error as err:
        print(f"Erreur MySQL : {err}")
        return jsonify({"error": str(err)}), 500

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT username, role FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user:
            return jsonify({"username": user['username'], "role": user['role'], "token": "fake-jwt-token"})
        return jsonify({"error": "Invalid credentials"}), 401
    except mysql.connector.Error as err:
        print(f"Erreur MySQL : {err}")
        return jsonify({"error": str(err)}), 500

@app.route('/articles', methods=['POST'])
def add_article():
    try:
        token = request.headers.get('Authorization')
        if not token or token != "Bearer fake-jwt-token":
            return jsonify({"error": "Unauthorized"}), 401
        data = request.get_json()
        title = data.get('title')
        summary = data.get('summary')
        category_id = data.get('category_id')
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO articles (title, summary, category_id) VALUES (%s, %s, %s)",
            (title, summary, category_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Article added"}), 201
    except mysql.connector.Error as err:
        print(f"Erreur MySQL : {err}")
        return jsonify({"error": str(err)}), 500

@app.route('/articles/<int:id>', methods=['PUT'])
def update_article(id):
    try:
        token = request.headers.get('Authorization')
        if not token or token != "Bearer fake-jwt-token":
            return jsonify({"error": "Unauthorized"}), 401
        data = request.get_json()
        title = data.get('title')
        summary = data.get('summary')
        category_id = data.get('category_id')
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE articles SET title = %s, summary = %s, category_id = %s WHERE id = %s",
            (title, summary, category_id, id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Article updated"})
    except mysql.connector.Error as err:
        print(f"Erreur MySQL : {err}")
        return jsonify({"error": str(err)}), 500

@app.route('/articles/<int:id>', methods=['DELETE'])
def delete_article(id):
    try:
        token = request.headers.get('Authorization')
        if not token or token != "Bearer fake-jwt-token":
            return jsonify({"error": "Unauthorized"}), 401
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM articles WHERE id = %s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Article deleted"})
    except mysql.connector.Error as err:
        print(f"Erreur MySQL : {err}")
        return jsonify({"error": str(err)}), 500

@app.route('/categories', methods=['POST'])
def add_category():
    try:
        token = request.headers.get('Authorization')
        if not token or token != "Bearer fake-jwt-token":
            return jsonify({"error": "Unauthorized"}), 401
        data = request.get_json()
        name = data.get('name')
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO categories (name) VALUES (%s)", (name,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Category added"}), 201
    except mysql.connector.Error as err:
        print(f"Erreur MySQL : {err}")
        return jsonify({"error": str(err)}), 500

@app.route('/users', methods=['GET'])
def get_users():
    try:
        token = request.headers.get('Authorization')
        if not token or token != "Bearer fake-jwt-token":
            return jsonify({"error": "Unauthorized"}), 401
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT username, role FROM users")
        users = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(users)
    except mysql.connector.Error as err:
        print(f"Erreur MySQL : {err}")
        return jsonify({"error": str(err)}), 500

@app.route('/users', methods=['POST'])
def add_user():
    try:
        token = request.headers.get('Authorization')
        if not token or token != "Bearer fake-jwt-token":
            return jsonify({"error": "Unauthorized"}), 401
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        role = data.get('role')
        client = Client('http://localhost:5001/soap?wsdl')
        result = client.service.AddUser(username, password, role)
        return jsonify({"message": result})
    except Exception as err:
        print(f"Erreur : {err}")
        return jsonify({"error": str(err)}), 500

@app.route('/users/<username>', methods=['PUT'])
def update_user(username):
    try:
        token = request.headers.get('Authorization')
        if not token or token != "Bearer fake-jwt-token":
            return jsonify({"error": "Unauthorized"}), 401
        data = request.get_json()
        password = data.get('password')
        role = data.get('role')
        client = Client('http://localhost:5001/soap?wsdl')
        result = client.service.UpdateUser(username, password, role)
        return jsonify({"message": result})
    except Exception as err:
        print(f"Erreur : {err}")
        return jsonify({"error": str(err)}), 500

@app.route('/users/<username>', methods=['DELETE'])
def delete_user(username):
    try:
        token = request.headers.get('Authorization')
        if not token or token != "Bearer fake-jwt-token":
            return jsonify({"error": "Unauthorized"}), 401
        client = Client('http://localhost:5001/soap?wsdl')
        result = client.service.DeleteUser(username)
        return jsonify({"message": result})
    except Exception as err:
        print(f"Erreur : {err}")
        return jsonify({"error": str(err)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)