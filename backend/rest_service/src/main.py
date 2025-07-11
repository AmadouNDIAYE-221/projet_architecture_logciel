# Fichier principal pour le service REST 
# backend/rest_service/src/main.py
from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        database="projet_al",
        user="root",
        password="votre_mot_de_passe",
        host="localhost"
    )

@app.route('/articles', methods=['GET'])
def get_articles():
    format = request.args.get('format', 'json')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, title, summary, category_id FROM articles")
    articles = cursor.fetchall()
    cursor.close()
    conn.close()
    if format == 'xml':
        # À implémenter : convertir en XML
        return jsonify({'message': 'XML non implémenté'})
    return jsonify(articles)

@app.route('/articles/category/<int:category_id>', methods=['GET'])
def get_articles_by_category(category_id):
    format = request.args.get('format', 'json')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, title, summary, category_id FROM articles WHERE category_id = %s", (category_id,))
    articles = cursor.fetchall()
    cursor.close()
    conn.close()
    if format == 'xml':
        return jsonify({'message': 'XML non implémenté'})
    return jsonify(articles)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)