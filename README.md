# Projet d'Architecture Logicielle
# Groupe 1 - Classe MASTER1

## Structure du projet
- **backend/** : Services web SOAP et REST, base de données
- **frontend/** : Site web avec interface utilisateur
- **client_app/** : Application cliente pour gérer les utilisateurs

## Instructions
1. Vérifiez que les informations du groupe et de la classe sont correctes.
2. Initialiser un dépôt Git et pousser sur un dépôt public.
3. Envoyer le lien du dépôt à envoitp@gmail.com avec l'objet "Projet_AL_Groupe_1_MASTER1".


Instructions pour démarrer le service REST : cd backend/rest_service/src && python main.py.
Instructions pour démarrer le service SOAP : cd backend/soap_service/src && python main.py.
Instructions pour tester le client SOAP : 
    \venv\Scripts\activate
    cd client_app/src && python main.py.
Instructions pour tester le frontend : cd frontend/public && python -m http.server 8000.