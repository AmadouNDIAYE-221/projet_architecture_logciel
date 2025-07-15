Projet_AL_Groupe_1_MASTER1
Ce projet est une application web pour la gestion d'articles, avec des fonctionnalités pour les visiteurs, éditeurs, et administrateurs. Il utilise un backend REST et SOAP, une base de données MySQL, et un frontend basé sur HTML, JavaScript, et Tailwind CSS.
Structure du projet

backend/ : Contient les services REST et SOAP.
database/ : Schéma (schema.sql) et données initiales (seed.sql) pour MySQL.
rest_service/src/ : API REST (Flask) pour gérer articles, catégories, et utilisateurs.
soap_service/src/ : Service SOAP pour l'authentification et la gestion des utilisateurs.


client_app/src/ : Client Python pour interagir avec le service SOAP.
frontend/ :
public/ : Fichiers statiques (HTML, JS, CSS) pour l'interface utilisateur.
src/components/ : Composants React (par exemple, AdminDashboard.js).


requirements.txt : Dépendances Python.
.gitignore : Exclut les fichiers temporaires et générés (venv/, node_modules/, etc.).
structure_projet.txt : Description de la structure du projet.

Prérequis

Python 3.8+ : Pour le backend et le client SOAP.
Node.js 14+ : Pour Tailwind CSS et les dépendances frontend.
MySQL 8.0+ : Pour la base de données.
Git : Pour cloner le dépôt.
Navigateur web : Chrome, Firefox, ou Edge pour tester le frontend.

Configuration
1. Cloner le dépôt
git clone https://github.com/<ton-utilisateur>/Projet_AL_Groupe_1_MASTER1.git
cd Projet_AL_Groupe_1_MASTER1

2. Configurer l’environnement virtuel Python

Créer et activer un environnement virtuel :python -m venv venv
.\venv\Scripts\activate


Installer les dépendances Python :pip install -r requirements.txt



3. Configurer MySQL

Accéder à MySQL :mysql -u root -p


Créer la base de données projet_al :CREATE DATABASE projet_al;


Configurer l’utilisateur root (remplace <mot_de_passe> par ton mot de passe, par exemple wtxLUd69i) :ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '<mot_de_passe>';
FLUSH PRIVILEGES;


Importer le schéma et les données initiales :mysql -u root -p projet_al < backend/database/schema.sql
mysql -u root -p projet_al < backend/database/seed.sql


Vérifier les tables :USE projet_al;
SHOW TABLES;


Tables attendues : users, categories, articles, tokens.


Vérifier les données :SELECT * FROM categories;
SELECT id, title, summary, category_id FROM articles;
SELECT username, role FROM users;


Catégories (exemple attendu, 13 lignes) :+----+-------------+
| id | name        |
+----+-------------+
| 1  | Culture     |
| 2  | Économie    |
| 22 | Test        |
| 25 | Test        |
| ...| ...         |
+----+-------------+


Articles (exemple attendu, 4 lignes) :+----+-------------------+----------------------------+-------------+
| id | title             | summary                    | category_id |
+----+-------------------+----------------------------+-------------+
| 1  | Article Culture 1 | Résumé de l'article...     | 1           |
| 2  | Article Culture 2 | Un autre article culturel  | 1           |
| 3  | Article Économie 1| Résumé économique          | 2           |
| 4  | ...               | ...                        | ...         |
+----+-------------------+----------------------------+-------------+


Utilisateurs (exemple attendu) :INSERT INTO users (username, password, role) VALUES
('editor1', '<hash_de_password123>', 'editeur'),
('admin1', '<hash_de_password123>', 'administrateur');


Note : Les mots de passe doivent être hachés (par exemple, avec bcrypt). Si seed.sql ne contient pas ces utilisateurs, ajoute-les manuellement ou mets à jour seed.sql.





4. Configurer le frontend (Tailwind CSS)

Naviguer dans le dossier frontend/public :cd frontend\public


Initialiser un projet Node.js (si nécessaire) :npm init -y


Installer Tailwind CSS :npm install -D tailwindcss@3.4.3


Générer css/output.css :npx tailwindcss -i ./css/input.css -o ./css/output.css --minify



5. Activer le support des chemins longs (Windows)

Pour éviter les erreurs avec zeep (client SOAP) :reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\FileSystem" /v LongPathsEnabled /t REG_DWORD /d 1



Exécution
1. Lancer le service REST

Naviguer dans le dossier du service REST :cd backend\rest_service\src


Lancer le serveur Flask :python main.py


Le serveur s’exécute sur http://192.168.1.13:5000.
Vérifie les endpoints :curl -X GET http://192.168.1.13:5000/categories
curl -X GET http://192.168.1.13:5000/articles





2. Lancer le service SOAP

Naviguer dans le dossier du service SOAP :cd backend\soap_service\src


Lancer le serveur SOAP :python main.py


Le serveur s’exécute sur http://localhost:5001/soap.
Vérifie le WSDL :curl http://localhost:5001/soap?wsdl





3. Lancer le client SOAP

Naviguer dans le dossier du client :cd client_app\src


Exécuter le client :python main.py



4. Lancer le frontend

Naviguer dans le dossier frontend/public :cd frontend\public


Régénérer css/output.css (si modifié) :npx tailwindcss -i ./css/input.css -o ./css/output.css --minify


Lancer le serveur HTTP :python -m http.server 8000


Ouvre dans un navigateur :
http://localhost:8000/index.html (interface pour visiteurs).
http://localhost:8000/login.html (connexion pour éditeurs/administrateurs).
http://localhost:8000/gestion_categories.html (gestion des catégories, pour administrateurs).
http://localhost:8000/gestion_articles.html (gestion des articles, pour éditeurs/administrateurs).
http://localhost:8000/gestion_utilisateurs.html (gestion des utilisateurs, pour administrateurs).
http://localhost:8000/dashboard.html (tableau de bord administrateur).



Fonctionnalités

Visiteurs (non connectés) :
Consultation des articles sur index.html.
Filtrage par catégorie via <select id="category">.
Détails des articles dans une modale (<div id="articleModal">).
Lien "Se connecter" dans <div id="authStatus">.


Éditeurs (rôle : editeur) :
Authentification via login.html.
Redirection vers gestion_articles.html après connexion.
Gestion des articles (ajouter, modifier, supprimer) avec un tableau (ID, Titre, Résumé, Catégorie, Actions).
Gestion des catégories via gestion_categories.html (ajouter, modifier, supprimer).


Administrateurs (rôle : administrateur) :
Redirection vers dashboard.html après connexion.
Gestion des articles via gestion_articles.html (comme les éditeurs).
Gestion des utilisateurs via gestion_utilisateurs.html (lister, ajouter, modifier, supprimer).
Gestion des catégories via gestion_categories.html.


Connexion/Déconnexion :
Connexion via login.html (ex. username: admin1, password: password123).
Déconnexion supprime token et role de localStorage et redirige vers login.html.



Choses à modifier avant l’exécution

Mot de passe MySQL :
Remplace <mot_de_passe> dans la configuration MySQL par ton mot de passe root (par exemple, wtxLUd69i).
Mets à jour backend/rest_service/src/main.py si nécessaire pour inclure les informations d’identification MySQL :mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '<mot_de_passe>',
    'database': 'projet_al'
}




Données initiales :
Vérifie backend/database/seed.sql pour t’assurer qu’il inclut des utilisateurs de test (editor1, admin1) avec des mots de passe hachés (par exemple, avec bcrypt).
Si nécessaire, ajoute manuellement :INSERT INTO users (username, password, role) VALUES
('editor1', '<hash_de_password123>', 'editeur'),
('admin1', '<hash_de_password123>', 'administrateur');


Exemple de hachage avec Python (bcrypt) :import bcrypt
password = "password123".encode('utf-8')
hashed = bcrypt.hashpw(password, bcrypt.gensalt())
print(hashed)




URL du backend :
Vérifie que les URLs dans les fichiers JavaScript (main.js, gestion_categories.js, etc.) pointent vers http://192.168.1.13:5000 (ou l’adresse de ton serveur REST).
Exemple dans main.js :fetch('http://192.168.1.13:5000/categories')


Si tu utilises une autre adresse IP ou localhost, mets à jour les fichiers :notepad frontend\public\js\main.js
notepad frontend\public\js\gestion_categories.js
notepad frontend\public\js\gestion_articles.js
notepad frontend\public\js\gestion_utilisateurs.js




Fichiers générés :
Régénère frontend/public/css/output.css avant de lancer le frontend :cd frontend\public
npx tailwindcss -i ./css/input.css -o ./css/output.css --minify




Fichier .gitignore :
Vérifie que .gitignore exclut les fichiers temporaires/générés :venv/
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.log
*.sqlite
frontend/public/css/output.css
frontend/public/node_modules/
frontend/public/package-lock.json
backend/rest_service/src/__pycache__/
backend/soap_service/src/__pycache__/
client_app/src/__pycache__/
backup_projet_al.sql
Capture d’écran 2025-07-12 062841.png
.DS_Store





Débogage

Problèmes de connexion/déconnexion :

Vérifie la table users :SELECT username, password, role FROM users WHERE username IN ('editor1', 'admin1');


Teste la route /login :curl -X POST http://192.168.1.13:5000/login -H "Content-Type: application/json" -d "{\"username\":\"admin1\",\"password\":\"password123\"}"


Vérifie le service SOAP :curl http://localhost:5001/soap?wsdl


Vérifie les logs de la console (F12 > Console) :Initialisation de navigation.js
Rôle détecté: administrateur
Clic sur: Déconnexion
Déconnexion : suppression de token et role
localStorage après déconnexion: null null
Redirection vers login.html
Initialisation de main.js
État initial { token: null, role: null }
Utilisateur non connecté


Vérifie localStorage (F12 > Application > Local Storage) avant/après déconnexion.
Vérifie les fichiers JavaScript :type frontend\public\js\login.js
type frontend\public\js\navigation.js
type frontend\public\js\main.js
type frontend\public\js\gestion_utilisateurs.js
type frontend\public\js\gestion_categories.js
type frontend\public\js\gestion_articles.js


Efface le cache du navigateur : F12 > Application > Clear Storage.


Problèmes d’affichage des articles/catégories :

Vérifie la console (F12 > Console) pour :Initialisation de main.js
État initial { token: null, role: null }
Utilisateur non connecté
Chargement des catégories
Réponse fetch /categories 200
Catégories chargées [{"id": 1, "name": "Culture"}, {"id": 22, "name": "Test"}, ...]
Chargement des articles
Réponse fetch /articles 200
Articles chargés [{"id": 1, "title": "Article Culture 1", ...}, ...]


Teste les endpoints :curl -X GET http://192.168.1.13:5000/categories
curl -X GET http://192.168.1.13:5000/articles
curl -X POST http://192.168.1.13:5000/categories -H "Authorization: Bearer <token>" -H "Content-Type: application/json" -d "{\"name\":\"Test\"}"


Vérifie les tables MySQL :SELECT * FROM categories;
SELECT id, title, summary, category_id FROM articles;


Erreur JavaScript (TypeError) :
Si Uncaught TypeError: Cannot read properties of null (reading 'addEventListener') ou Élément <id> non trouvé apparaît :
Vérifie les ID dans index.html : category, articles, authStatus, articleModal, modalTitle, modalSummary, modalCategory.
Vérifie les ID dans gestion_categories.html : categoriesTableBody, addCategoryButton, categoryForm, categoryModal, categoryName, categoryId, modalTitle.
Compare avec main.js et gestion_categories.js pour t’assurer que les ID correspondent.
Remplace main.js ou gestion_categories.js par les versions corrigées si nécessaire.


Efface le cache du navigateur : F12 > Application > Clear Storage.


Vérifie les fichiers servis :dir frontend\public\dashboard.html
dir frontend\public\index.html
dir frontend\public\gestion_categories.html
dir frontend\public\gestion_articles.html
dir frontend\public\gestion_utilisateurs.html




Problèmes Git :

Vérifie l’état du dépôt :git status


Ajoute toutes les modifications :git add .
git commit -m "Mise à jour complète du projet"
git push origin main


Résous les conflits si nécessaire :git pull origin main
git add <fichier_conflit>
git commit
git push origin main





Gestion des fichiers générés

css/output.css : Régénéré automatiquement avec Tailwind CSS. Exclu via .gitignore.
node_modules/ : Installé avec npm install. Exclu via .gitignore.
pycache/ : Fichiers compilés Python. Exclus via .gitignore.
backup_projet_al.sql : Sauvegarde de la base de données, à ne pas versionner.

Contribution

Crée une branche pour tes modifications :git checkout -b feature/<nom_feature>


Ajoute et valide tes modifications :git add .
git commit -m "Ajout de <description>"


Pousse la branche et crée une pull request :git push origin feature/<nom_feature>



Problèmes courants

Erreur MySQL "Access denied" : Vérifie le mot de passe dans backend/rest_service/src/main.py.
Erreur 404 sur les endpoints REST : Vérifie que le serveur Flask est en cours d’exécution (http://192.168.1.13:5000).
Erreur JavaScript dans la console : Vérifie les ID dans les fichiers HTML et JS.
Fichiers non affichés : Efface le cache du navigateur ou régénère css/output.css.
