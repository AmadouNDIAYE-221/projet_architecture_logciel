# backend\soap_service\src\auth_service.py
import mysql.connector
import bcrypt
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            database="projet_al",
            user="root",
            password="wtxLUd69i",
            host="localhost",
            auth_plugin="mysql_native_password"
        )
        logger.info("Connexion à la base de données établie avec succès.")
        return conn
    except mysql.connector.Error as err:
        logger.error(f"Erreur de connexion MySQL : {err}")
        raise

def authenticate(username, password):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        logger.info(f"Utilisateur récupéré pour {username}: {user}")
        cursor.close()
        conn.close()

        if not user:
            logger.warning(f"Aucun utilisateur trouvé pour {username}")
            return 'none'

        password_match = bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8'))
        logger.info(f"Vérification du mot de passe pour {username}: {password_match}")
        
        if password_match:
            logger.info(f"Authentification réussie pour {username}, rôle: {user['role']}")
            return user['role']
        else:
            logger.warning(f"Échec de l'authentification pour {username}: mot de passe incorrect")
            return 'none'
    except mysql.connector.Error as err:
        logger.error(f"Erreur MySQL lors de l'authentification : {err}")
        return 'none'
    except Exception as e:
        logger.error(f"Erreur inattendue lors de l'authentification : {e}")
        return 'none'