# backend/soap_service/src/main.py
from flask import Flask
from spyne import Application, ServiceBase, Unicode, Integer, ComplexModel, rpc
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        database="projet_al",
        user="root",
        password="wtxLUd69i",  
        host="localhost",
        auth_plugin="mysql_native_password"
    )

class User(ComplexModel):
    username = Unicode
    role = Unicode

class UserService(ServiceBase):
    @rpc(Unicode, _returns=User)
    def GetUser(ctx, username):
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT username, role FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            cursor.close()
            conn.close()
            if user:
                return User(username=user['username'], role=user['role'])
            return User(username=username, role="not found")
        except mysql.connector.Error as err:
            raise Exception(str(err))

    @rpc(Unicode, Unicode, Unicode, _returns=Unicode)
    def AddUser(ctx, username, password, role):
        try:
            if role not in ['editor', 'admin']:
                return "Invalid role"
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
                (username, password, role)
            )
            conn.commit()
            cursor.close()
            conn.close()
            return "User added"
        except mysql.connector.Error as err:
            return str(err)

    @rpc(Unicode, Unicode, Unicode, _returns=Unicode)
    def UpdateUser(ctx, username, password, role):
        try:
            if role not in ['editor', 'admin']:
                return "Invalid role"
            conn = get_db_connection()
            cursor = conn.cursor()
            if password:
                cursor.execute(
                    "UPDATE users SET password = %s, role = %s WHERE username = %s",
                    (password, role, username)
                )
            else:
                cursor.execute(
                    "UPDATE users SET role = %s WHERE username = %s",
                    (role, username)
                )
            if cursor.rowcount == 0:
                cursor.close()
                conn.close()
                return "User not found"
            conn.commit()
            cursor.close()
            conn.close()
            return "User updated"
        except mysql.connector.Error as err:
            return str(err)

    @rpc(Unicode, _returns=Unicode)
    def DeleteUser(ctx, username):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE username = %s", (username,))
            if cursor.rowcount == 0:
                cursor.close()
                conn.close()
                return "User not found"
            conn.commit()
            cursor.close()
            conn.close()
            return "User deleted"
        except mysql.connector.Error as err:
            return str(err)

application = Application(
    [UserService],
    tns='projet_al',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)
wsgi_app = WsgiApplication(application)
app.wsgi_app = wsgi_app

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)