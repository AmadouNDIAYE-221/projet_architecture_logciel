# client_app\src\user_management.py
import zeep
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UserManagementClient:
    def __init__(self, wsdl_url="http://localhost:5001/soap?wsdl"):
        try:
            self.client = zeep.Client(wsdl_url)
            logger.info("Client SOAP pour gestion des utilisateurs initialisé avec succès.")
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation du client SOAP : {e}")
            raise

    def list_users(self):
        try:
            users = self.client.service.listUsers()
            logger.info(f"Réponse brute de listUsers : {users}")
            if users is None or not users:
                logger.warning("Aucun utilisateur retourné par listUsers.")
                return []
            if not isinstance(users, list):
                logger.warning(f"Réponse inattendue de listUsers : type={type(users)}, valeur={users}")
                return []
            logger.info(f"Liste des utilisateurs récupérée avec succès : {len(users)} utilisateurs.")
            result = []
            for user in users:
                try:
                    result.append({"id": user.id, "username": user.username, "role": user.role})
                except AttributeError as e:
                    logger.error(f"Erreur lors de la conversion d'un utilisateur : {e}")
                    continue
            return result
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des utilisateurs : {e}")
            return []

    def add_user(self, username, password, role):
        try:
            success = self.client.service.addUser(username, password, role)
            if success:
                logger.info(f"Utilisateur {username} ajouté avec succès.")
            else:
                logger.warning(f"Échec de l'ajout de l'utilisateur {username}.")
            return success
        except Exception as e:
            logger.error(f"Erreur lors de l'ajout de l'utilisateur {username} : {e}")
            return False

    def update_user(self, id, username, password, role):
        try:
            success = self.client.service.updateUser(id, username, password, role)
            if success:
                logger.info(f"Utilisateur ID {id} mis à jour avec succès.")
            else:
                logger.warning(f"Échec de la mise à jour de l'utilisateur ID {id}.")
            return success
        except Exception as e:
            logger.error(f"Erreur lors de la mise à jour de l'utilisateur ID {id} : {e}")
            return False

    def delete_user(self, id):
        try:
            success = self.client.service.deleteUser(id)
            if success:
                logger.info(f"Utilisateur ID {id} supprimé avec succès.")
            else:
                logger.warning(f"Échec de la suppression de l'utilisateur ID {id}.")
            return success
        except Exception as e:
            logger.error(f"Erreur lors de la suppression de l'utilisateur ID {id} : {e}")
            return False