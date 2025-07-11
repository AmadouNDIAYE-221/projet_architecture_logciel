# backend/rest_service/src/main.py
from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

def get_db_connection():
    return mysql.connector.connect(
        database="projet_al",
        user="root",
        password="wtxLUd69i",  # Mettez à jour avec le mot de passe correct
        host="localhost",
        auth_plugin="mysql_native_password"  # Spécifiez explicitement le plugin
    )

@app.route('/articles', methods=['GET'])
def get_articles():
    try:
        page = int(request.args.get('page', 1))
        if page < 1:
            page = 1
        per_page = 10
        offset = (page - 1) * per_page
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, title, summary, category_id FROM articles LIMIT %s OFFSET %s", (per_page, offset))
        articles = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(articles)
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    except ValueError:
        return jsonify({"error": "Invalid page parameter"}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)