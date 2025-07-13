# client_app\src\auth_client.py
import zeep
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AuthClient:
    def __init__(self, wsdl_url="http://localhost:5001/soap?wsdl"):
        try:
            self.client = zeep.Client(wsdl_url)
            logger.info("Client SOAP initialisé avec succès.")
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation du client SOAP : {e}")
            raise

    def authenticate(self, username, password):
        try:
            role = self.client.service.authenticate(username, password)
            logger.info(f"Authentification réussie pour {username}, rôle : {role}")
            return role
        except Exception as e:
            logger.error(f"Erreur lors de l'authentification pour {username} : {e}")
            return 'none'