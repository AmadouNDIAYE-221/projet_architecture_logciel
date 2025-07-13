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
    .\venv\Scripts\activate
    cd client_app/src && python main.py.
Instructions pour tester le frontend : cd frontend/public && python -m http.server 8000.

# Projet_AL_Groupe_1_MASTER1
## Configuration
1. Active l'environnement : `.\venv\Scripts\activate`
2. Installe les dépendances : `pip install -r requirements.txt`
3. Configure MySQL :
   - `mysql -u root -p projet_al < backend/database/schema.sql`
   - `mysql -u root -p projet_al < backend/database/seed.sql`
   - `ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'votre_nouveau_mot_de_passe';`
## Exécution
- REST : `cd backend/rest_service/src && python main.py`
- SOAP : `cd backend/soap_service/src && python main.py`
- Client SOAP : `cd client_app/src && python main.py`
- Frontend : `cd frontend/public && python -m http.server 8000`
## Notes
- Patches pour `spyne` :
  - `venv\Lib\site-packages\spyne\util\oset.py` : `from collections.abc import MutableSet`
  - `venv\Lib\site-packages\spyne\service.py` : `from collections.abc import Sequence`
  - `venv\Lib\site-packages\spyne\protocol\dictdoc\hier.py` : `from collections.abc import Iterable as AbcIterable`
- Alternative : `spyne==2.11.0`


# Projet_AL_Groupe_1_MASTER1
## Configuration
1. Active l'environnement : `.\venv\Scripts\activate`
2. Installe les dépendances : `pip install -r requirements.txt`
3. Configure MySQL :
   - `mysql -u root -p projet_al < backend/database/schema.sql`
   - `mysql -u root -p projet_al < backend/database/seed.sql`
   - `ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'votre_nouveau_mot_de_passe';`
   - Mets à jour les mots de passe hachés : génère avec `bcrypt` et utilise `UPDATE users SET password = 'valeur_hachée'`.
## Exécution
- REST : `cd backend/rest_service/src && python main.py`
- SOAP : `cd backend/soap_service/src && python main.py`
- Client SOAP : `cd client_app/src && python main.py`
- Frontend : `cd frontend/public && python -m http.server 8000`
## Fonctionnalités
- Visiteurs simples : Consultation articles/filtrage (`http://localhost:8000`).
- Éditeurs : Authentification (`http://localhost:8000/login.html`), gestion articles/catégories.
- Administrateurs : Gestion utilisateurs via SOAP (`http://localhost:5001/soap`).
## Notes
- Patches pour `spyne` :
  - `venv\Lib\site-packages\spyne\util\oset.py` : `from collections.abc import MutableSet`
  - `venv\Lib\site-packages\spyne\service.py` : `from collections.abc import Sequence`
  - `venv\Lib\site-packages\spyne\protocol\dictdoc\hier.py` : `from collections.abc import Iterable as AbcIterable`
- Utilise `bcrypt` pour hacher/vérifier les mots de passe dans `backend/rest_service/src/main.py`.




# Projet_AL_Groupe_1_MASTER1

## Configuration
1. Activez l'environnement virtuel : `.\venv\Scripts\activate`
2. Installez les dépendances : `pip install -r requirements.txt`
3. Configurez MySQL :
   - Créez la base de données : `mysql -u root -p projet_al < backend/database/schema.sql`
   - Ajoutez des données : `mysql -u root -p projet_al < backend/database/seed.sql`
   - Configurez l'utilisateur root : `ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'votre_nouveau_mot_de_passe';`

## Exécution
- Service REST : `cd backend/rest_service/src && python main.py`
- Service SOAP : `cd backend/soap_service/src && python main.py`
- Client SOAP : `cd client_app/src && python main.py`
- Frontend : `cd frontend/public && python -m http.server 8000`

## Fonctionnalités
- **Visiteurs simples** : Consultation des articles et filtrage par catégorie sans authentification (`http://localhost:8000`).
- **Éditeurs** : Authentification (`http://localhost:8000/login.html`) et gestion (lister, ajouter, modifier, supprimer) des articles et catégories.
- **Administrateurs** : Gestion des utilisateurs (lister, ajouter, modifier, supprimer) via le service SOAP (`http://localhost:5001/soap`) avec un panneau d'administration élégant à onglets.
- **Catégories** : Culture, Économie, Éducation, Environnement, Politique, Santé, Sciences, Sport, Technologie, Voyage.

## Notes
- Activez le support des chemins longs pour `zeep` (Regedit: `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\FileSystem`, `LongPathsEnabled=1`).
- MySQL doit utiliser `mysql_native_password` pour `root`.
- Accédez à la page de connexion : `http://localhost:8000/login.html` (non requis pour les visiteurs simples).