# rest_service/src/category_controller.py

from flask import Blueprint, request, jsonify
from utils import get_db_connection, verify_token


category_bp = Blueprint('category_bp', __name__)

@category_bp.route('/categories', methods=['GET'])
def get_categories():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, name FROM categories")
        categories = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(categories)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@category_bp.route('/categories', methods=['POST'])
def add_category():
    payload = verify_token(['administrateur', 'editeur'])
    if not payload:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    name = data.get('name')
    if not name:
        return jsonify({'error': 'Nom requis'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO categories (name) VALUES (%s)", (name,))
        conn.commit()
        category_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return jsonify({'id': category_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@category_bp.route('/categories/<int:id>', methods=['PUT'])
def update_category(id):
    payload = verify_token(['administrateur', 'editeur'])
    if not payload:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    name = data.get('name')
    if not name:
        return jsonify({'error': 'Nom requis'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE categories SET name = %s WHERE id = %s", (name, id))
        conn.commit()
        success = cursor.rowcount > 0
        cursor.close()
        conn.close()
        return jsonify({'success': success}), 200 if success else 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@category_bp.route('/categories/<int:id>', methods=['DELETE'])
def delete_category(id):
    payload = verify_token(['administrateur', 'editeur'])
    if not payload:
        return jsonify({'error': 'Unauthorized'}), 401

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM categories WHERE id = %s", (id,))
        conn.commit()
        success = cursor.rowcount > 0
        cursor.close()
        conn.close()
        return jsonify({'success': success}), 200 if success else 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
