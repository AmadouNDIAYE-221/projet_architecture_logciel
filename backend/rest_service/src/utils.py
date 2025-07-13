# rest_service/src/utils.py

import mysql.connector
import jwt
from flask import request

SECRET_KEY = "your-secret-key"

def get_db_connection():
    return mysql.connector.connect(
        database="projet_al",
        user="root",
        password="wtxLUd69i",
        host="localhost",
        auth_plugin="mysql_native_password"
    )

def verify_token(required_roles=None):
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        if required_roles and payload['role'] not in required_roles:
            return None
        return payload
    except jwt.InvalidTokenError:
        return None
