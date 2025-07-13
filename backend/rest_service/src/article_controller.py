# rest_service/src/article_controller.py

from flask import Blueprint, request, jsonify
from utils import get_db_connection, verify_token


article_bp = Blueprint('article_bp', __name__)

@article_bp.route('/articles', methods=['GET'])
def get_articles():
    try:
        page = int(request.args.get('page', 1))
        category = request.args.get('category')
        per_page = 10
        offset = (page - 1) * per_page

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        if category:
            cursor.execute("SELECT * FROM articles WHERE category_id = %s LIMIT %s OFFSET %s", (category, per_page, offset))
        else:
            cursor.execute("SELECT * FROM articles LIMIT %s OFFSET %s", (per_page, offset))

        articles = cursor.fetchall()
        cursor.close()
        conn.close()

        return jsonify(articles)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@article_bp.route('/articles', methods=['POST'])
def add_article():
    payload = verify_token(['administrateur', 'editeur'])
    if not payload:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    title = data.get('title')
    summary = data.get('summary')
    category_id = data.get('category_id')

    if not all([title, summary, category_id]):
        return jsonify({'error': 'Champs manquants'}), 400

    try:
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
        return jsonify({'id': article_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@article_bp.route('/articles/<int:id>', methods=['PUT'])
def update_article(id):
    payload = verify_token(['administrateur', 'editeur'])
    if not payload:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    title = data.get('title')
    summary = data.get('summary')
    category_id = data.get('category_id')

    if not all([title, summary, category_id]):
        return jsonify({'error': 'Champs manquants'}), 400

    try:
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
        return jsonify({'success': success}), 200 if success else 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@article_bp.route('/articles/<int:id>', methods=['DELETE'])
def delete_article(id):
    payload = verify_token(['administrateur', 'editeur'])
    if not payload:
        return jsonify({'error': 'Unauthorized'}), 401

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM articles WHERE id = %s", (id,))
        conn.commit()
        success = cursor.rowcount > 0
        cursor.close()
        conn.close()
        return jsonify({'success': success}), 200 if success else 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
