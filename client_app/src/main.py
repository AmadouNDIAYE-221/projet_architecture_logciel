# Fichier principal pour l'application cliente 
# client_app/src/main.py
from zeep import Client

client = Client('http://localhost:5001/soap?wsdl')
result = client.service.GetUser('admin1')
print(result)