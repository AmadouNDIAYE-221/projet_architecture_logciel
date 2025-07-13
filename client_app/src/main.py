# client_app\src\main.py
from auth_client import AuthClient
from user_management import UserManagementClient
import traceback

def main():
    try:
        auth_client = AuthClient()
        user_client = UserManagementClient()
        username = "admin1"
        password = "password123"
        role = auth_client.authenticate(username, password)
        print(f"Résultat de l'authentification pour {username} : {role}")
        users = user_client.list_users()
        print("\nListe des utilisateurs :")
        if users:
            for user in users:
                print(f"ID: {user['id']}, Username: {user['username']}, Role: {user['role']}")
        else:
            print("Aucun utilisateur trouvé.")
        new_username = "testuser"
        new_password = "testpass123"
        new_role = "visiteur"
        success = user_client.add_user(new_username, new_password, new_role)
        print(f"\nAjout de l'utilisateur {new_username} : {'Succès' if success else 'Échec'}")
        success = user_client.update_user(1, "admin_updated", "newpass123", "administrateur")
        print(f"Mise à jour de l'utilisateur ID 1 : {'Succès' if success else 'Échec'}")
        success = user_client.delete_user(1)
        print(f"Suppression de l'utilisateur ID 1 : {'Succès' if success else 'Échec'}")
    except Exception as e:
        print(f"Erreur lors de l'appel SOAP : {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()