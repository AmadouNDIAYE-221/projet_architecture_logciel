import bcrypt
from spyne import ServiceBase, Application, rpc, Unicode, Iterable, ComplexModel, Integer
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server
import mysql.connector
from mysql.connector import Error

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            database='projet_al',
            user='root',
            password='wtxLUd69i',
            auth_plugin='mysql_native_password'
        )
        return conn
    except Error as e:
        print(f"Erreur de connexion à MySQL: {e}")
        return None

# Définir un modèle complexe pour l'utilisateur
class User(ComplexModel):
    id = Integer
    username = Unicode
    role = Unicode

class UserService(ServiceBase):
    @rpc(Unicode, Unicode, _returns=Unicode)
    def authenticate(ctx, username, password):
        try:
            conn = get_db_connection()
            if conn is None:
                print("Connexion à la base de données échouée")
                return None
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT role, password FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            conn.close()
            if user:
                print(f"Utilisateur trouvé : {username}, rôle: {user['role']}, hachage: {user['password']}")
                if bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
                    print(f"Authentification réussie pour {username}, rôle: {user['role']}")
                    return user['role']
                else:
                    print(f"Échec de l'authentification pour {username}: mot de passe incorrect")
                    return None
            else:
                print(f"Échec de l'authentification pour {username}: utilisateur non trouvé")
                return None
        except Exception as e:
            print(f"Erreur dans authenticate: {e}")
            return None

    @rpc(_returns=Iterable(User))
    def listUsers(ctx):
        try:
            conn = get_db_connection()
            if conn is None:
                print("Connexion à la base de données échouée")
                return []
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id, username, role FROM users")
            users_data = cursor.fetchall()
            
            # Mapper les rôles vers le format attendu
            role_mapping = {
                'administrateur': 'admin',
                'editeur': 'editor',
                'visiteur': 'visitor'
            }
            
            users = []
            for user_data in users_data:
                user = User()
                user.id = user_data['id']
                user.username = user_data['username']
                user.role = role_mapping.get(user_data['role'], user_data['role'])
                users.append(user)
            
            print(f"Nombre d'utilisateurs trouvés: {len(users)}")
            print(f"Données formatées: {[(u.id, u.username, u.role) for u in users]}")
            conn.close()
            return users
        except Exception as e:
            print(f"Erreur dans listUsers: {e}")
            return []

    @rpc(Unicode, Unicode, Unicode, _returns=Unicode)
    def addUser(ctx, username, password, role):
        try:
            conn = get_db_connection()
            if conn is None:
                return "false"
            cursor = conn.cursor()
            
            # Mapper les rôles du format REST vers le format DB
            role_mapping = {
                'admin': 'administrateur',
                'editor': 'editeur',
                'visitor': 'visiteur'
            }
            db_role = role_mapping.get(role, role)
            
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", 
                          (username, hashed_password, db_role))
            conn.commit()
            conn.close()
            print(f"Utilisateur ajouté: {username} avec le rôle {db_role}")
            return "true"
        except Exception as e:
            print(f"Erreur dans addUser: {e}")
            return "false"

    @rpc(Integer, Unicode, Unicode, Unicode, _returns=Unicode)
    def updateUser(ctx, user_id, username, password, role):
        try:
            conn = get_db_connection()
            if conn is None:
                return "false"
            cursor = conn.cursor()
            
            # Mapper les rôles du format REST vers le format DB
            role_mapping = {
                'admin': 'administrateur',
                'editor': 'editeur',
                'visitor': 'visiteur'
            }
            db_role = role_mapping.get(role, role)
            
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            cursor.execute("UPDATE users SET username = %s, password = %s, role = %s WHERE id = %s", 
                          (username, hashed_password, db_role, user_id))
            conn.commit()
            conn.close()
            print(f"Utilisateur mis à jour: {username} avec le rôle {db_role}")
            return "true"
        except Exception as e:
            print(f"Erreur dans updateUser: {e}")
            return "false"

    @rpc(Integer, _returns=Unicode)
    def deleteUser(ctx, user_id):
        try:
            conn = get_db_connection()
            if conn is None:
                return "false"
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
            conn.commit()
            conn.close()
            print(f"Utilisateur supprimé: ID {user_id}")
            return "true"
        except Exception as e:
            print(f"Erreur dans deleteUser: {e}")
            return "false"

# Initialisation de la base de données
def init_db():
    try:
        conn = get_db_connection()
        if conn is None:
            print("Connexion à la base de données échouée")
            return
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                role VARCHAR(50) NOT NULL
            )
        ''')
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            hashed_password = bcrypt.hashpw('password123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            cursor.executemany("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", [
                ('admin1', hashed_password, 'administrateur'),
                ('editor1', hashed_password, 'editeur'),
                ('visitor1', hashed_password, 'visiteur')
            ])
            conn.commit()
        conn.close()
        print("Base de données initialisée avec succès")
    except Exception as e:
        print(f"Erreur lors de l'initialisation de la base de données: {e}")

application = Application(
    [UserService],
    tns='urn:user_service',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

if __name__ == '__main__':
    init_db()
    wsgi_app = WsgiApplication(application)
    server = make_server('0.0.0.0', 5001, wsgi_app)
    print("Serveur SOAP démarré sur http://localhost:5001/soap?wsdl")
    server.serve_forever()