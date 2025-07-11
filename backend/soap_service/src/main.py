# backend/soap_service/src/main.py
from flask import Flask, Response, request, send_file
import mysql.connector
from xml.etree import ElementTree as ET
import os

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        database="projet_al",
        user="root",
        password="wtxLUd69i",
        host="localhost"
    )

@app.route('/soap', methods=['POST'])
def soap_service():
    try:
        # Parser la requête SOAP
        xml_request = ET.fromstring(request.data)
        username = xml_request.find('.//username').text
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT username, role FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        
        # Créer une réponse SOAP
        response_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns="http://example.com/userservice">
    <soap:Body>
        <ns:GetUserResponse>
            <ns:user>{f"Username: {user[0]}, Role: {user[1]}" if user else "User not found"}</ns:user>
        </ns:GetUserResponse>
    </soap:Body>
</soap:Envelope>"""
        return Response(response_xml, mimetype='text/xml')
    except Exception as e:
        response_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
    <soap:Body>
        <soap:Fault>
            <faultcode>soap:Server</faultcode>
            <faultstring>{str(e)}</faultstring>
        </soap:Fault>
    </soap:Body>
</soap:Envelope>"""
        return Response(response_xml, mimetype='text/xml')

@app.route('/soap', methods=['GET'])
def get_wsdl():
    wsdl_path = os.path.join('..', 'config', 'wsdl', 'user_service.wsdl')
    return send_file(wsdl_path, mimetype='text/xml')

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5001)