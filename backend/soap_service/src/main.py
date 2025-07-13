from flask import Flask, Response
from spyne import Application, ServiceBase, Unicode, Integer, Boolean
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from spyne.model.complex import Array, ComplexModel
import mysql.connector
import bcrypt

app = Flask(__name__)

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

class User(ComplexModel):
    __namespace__ = 'http://example.com/userservice'
    id = Integer
    username = Unicode
    role = Unicode

wsdl = """
<definitions name="UserService"
    targetNamespace="http://example.com/userservice"
    xmlns:tns="http://example.com/userservice"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema"
    xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/"
    xmlns="http://schemas.xmlsoap.org/wsdl/">
    <message name="authenticateRequest">
        <part name="username" type="xsd:string"/>
        <part name="password" type="xsd:string"/>
    </message>
    <message name="authenticateResponse">
        <part name="role" type="xsd:string"/>
    </message>
    <message name="listUsersRequest"/>
    <message name="listUsersResponse">
        <part name="users" type="tns:UserArray"/>
    </message>
    <message name="addUserRequest">
        <part name="username" type="xsd:string"/>
        <part name="password" type="xsd:string"/>
        <part name="role" type="xsd:string"/>
    </message>
    <message name="addUserResponse">
        <part name="success" type="xsd:boolean"/>
    </message>
    <message name="updateUserRequest">
        <part name="id" type="xsd:int"/>
        <part name="username" type="xsd:string"/>
        <part name="password" type="xsd:string"/>
        <part name="role" type="xsd:string"/>
    </message>
    <message name="updateUserResponse">
        <part name="success" type="xsd:boolean"/>
    </message>
    <message name="deleteUserRequest">
        <part name="id" type="xsd:int"/>
    </message>
    <message name="deleteUserResponse">
        <part name="success" type="xsd:boolean"/>
    </message>
    <portType name="UserServicePortType">
        <operation name="authenticate">
            <input message="tns:authenticateRequest"/>
            <output message="tns:authenticateResponse"/>
        </operation>
        <operation name="listUsers">
            <input message="tns:listUsersRequest"/>
            <output message="tns:listUsersResponse"/>
        </operation>
        <operation name="addUser">
            <input message="tns:addUserRequest"/>
            <output message="tns:addUserResponse"/>
        </operation>
        <operation name="updateUser">
            <input message="tns:updateUserRequest"/>
            <output message="tns:updateUserResponse"/>
        </operation>
        <operation name="deleteUser">
            <input message="tns:deleteUserRequest"/>
            <output message="tns:deleteUserResponse"/>
        </operation>
    </portType>
    <binding name="UserServiceBinding" type="tns:UserServicePortType">
        <soap:binding style="rpc" transport="http://schemas.xmlsoap.org/soap/http"/>
        <operation name="authenticate">
            <soap:operation soapAction="authenticate"/>
            <input>
                <soap:body use="literal" namespace="http://example.com/userservice"/>
            </input>
            <output>
                <soap:body use="literal" namespace="http://example.com/userservice"/>
            </output>
        </operation>
        <operation name="listUsers">
            <soap:operation soapAction="listUsers"/>
            <input>
                <soap:body use="literal" namespace="http://example.com/userservice"/>
            </input>
            <output>
                <soap:body use="literal" namespace="http://example.com/userservice"/>
            </output>
        </operation>
        <operation name="addUser">
            <soap:operation soapAction="addUser"/>
            <input>
                <soap:body use="literal" namespace="http://example.com/userservice"/>
            </input>
            <output>
                <soap:body use="literal" namespace="http://example.com/userservice"/>
            </output>
        </operation>
        <operation name="updateUser">
            <soap:operation soapAction="updateUser"/>
            <input>
                <soap:body use="literal" namespace="http://example.com/userservice"/>
            </input>
            <output>
                <soap:body use="literal" namespace="http://example.com/userservice"/>
            </output>
        </operation>
        <operation name="deleteUser">
            <soap:operation soapAction="deleteUser"/>
            <input>
                <soap:body use="literal" namespace="http://example.com/userservice"/>
            </input>
            <output>
                <soap:body use="literal" namespace="http://example.com/userservice"/>
            </output>
        </operation>
    </binding>
    <service name="UserService">
        <port name="UserServicePort" binding="tns:UserServiceBinding">
            <soap:address location="http://localhost:5001/soap"/>
        </port>
    </service>
    <types>
        <xsd:schema targetNamespace="http://example.com/userservice">
            <xsd:complexType name="User">
                <xsd:sequence>
                    <xsd:element name="id" type="xsd:int"/>
                    <xsd:element name="username" type="xsd:string"/>
                    <xsd:element name="role" type="xsd:string"/>
                </xsd:sequence>
            </xsd:complexType>
            <xsd:complexType name="UserArray">
                <xsd:sequence>
                    <xsd:element name="user" type="tns:User" minOccurs="0" maxOccurs="unbounded"/>
                </xsd:sequence>
            </xsd:complexType>
        </xsd:schema>
    </types>
</definitions>
"""

@app.route('/soap')
def serve_wsdl():
    return Response(wsdl, content_type='text/xml')

def authenticate(username, password):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            print(f"Authentification réussie pour {username}, rôle: {user['role']}")
            return user['role']
        print(f"Échec de l'authentification pour {username}")
        return 'none'
    except mysql.connector.Error as err:
        print(f"Erreur MySQL : {err}")
        return 'none'

def listUsers():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, username, role FROM users")
        users = cursor.fetchall()
        print(f"Nombre d'utilisateurs trouvés: {len(users)}")
        print(f"Données brutes: {users}")
        cursor.close()
        conn.close()
        return [User(id=user['id'], username=user['username'], role=user['role']) for user in users]
    except mysql.connector.Error as err:
        print(f"Erreur MySQL : {err}")
        return []

def addUser(username, password, role):
    try:
        valid_roles = ['administrateur', 'editeur', 'visiteur']
        if role not in valid_roles:
            print(f"Rôle invalide : {role}")
            return False
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
            (username, hashed_password, role)
        )
        conn.commit()
        success = cursor.rowcount > 0
        cursor.close()
        conn.close()
        print(f"Ajout utilisateur : {username}, succès: {success}")
        return success
    except mysql.connector.Error as err:
        print(f"Erreur MySQL : {err}")
        return False

def updateUser(id, username, password, role):
    try:
        valid_roles = ['administrateur', 'editeur', 'visiteur']
        if role not in valid_roles:
            print(f"Rôle invalide : {role}")
            return False
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET username = %s, password = %s, role = %s WHERE id = %s",
            (username, hashed_password, role, id)
        )
        conn.commit()
        success = cursor.rowcount > 0
        cursor.close()
        conn.close()
        print(f"Mise à jour utilisateur ID {id}: {success}")
        return success
    except mysql.connector.Error as err:
        print(f"Erreur MySQL : {err}")
        return False

def deleteUser(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = %s", (id,))
        conn.commit()
        success = cursor.rowcount > 0
        cursor.close()
        conn.close()
        print(f"Suppression utilisateur ID {id}: {success}")
        return success
    except mysql.connector.Error as err:
        print(f"Erreur MySQL : {err}")
        return False

from spyne.decorator import rpc

class UserService(ServiceBase):
    @rpc(Unicode, Unicode, _returns=Unicode)
    def authenticate(ctx, username, password):
        return authenticate(username, password)

    @rpc(_returns=Array(User))
    def listUsers(ctx):
        return listUsers()

    @rpc(Unicode, Unicode, Unicode, _returns=Boolean)
    def addUser(ctx, username, password, role):
        return addUser(username, password, role)

    @rpc(Integer, Unicode, Unicode, Unicode, _returns=Boolean)
    def updateUser(ctx, id, username, password, role):
        return updateUser(id, username, password, role)

    @rpc(Integer, _returns=Boolean)
    def deleteUser(ctx, id):
        return deleteUser(id)

application = Application(
    [UserService],
    tns='http://example.com/userservice',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

wsgi_app = WsgiApplication(application)

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    server = make_server('0.0.0.0', 5001, wsgi_app)
    print("Serveur SOAP démarré sur http://localhost:5001/soap")
    server.serve_forever()