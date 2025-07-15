# Projet d'Architecture Logicielle
# Groupe 1 - Classe MASTER1
# Membres du groupes
- **Papa Amadou Mandiaye NDIAYE**
- **Aïssatou FOFANA**
- **Boubacar NIANF**
# Présentation
Ce projet est une application web pour la gestion d'articles, avec des fonctionnalités pour les visiteurs, éditeurs, et administrateurs. Il utilise un backend REST et SOAP, une base de données MySQL, et un frontend basé sur HTML, JavaScript, et Tailwind CSS.

## Structure du projet
- **backend/** : Services web SOAP et REST, base de données
- **frontend/** : Site web avec interface utilisateur
- **client_app/** : Application cliente pour gérer les utilisateurs


## Prérequis
- **Python 3.8+** : Pour le backend et le client SOAP.
- **Node.js 14+** : Pour Tailwind CSS et les dépendances frontend.
- **MySQL 8.0+** : Pour la base de données.
- **Git** : Pour cloner le dépôt.
- **Navigateur web** : Chrome, Firefox, ou Edge pour tester le frontend.

## Configuration
1. Cloner le dépôt
        git clone https://github.com/<ton-utilisateur>/Projet_AL_Groupe_1_MASTER1.git
        cd Projet_AL_Groupe_1_MASTER1

2. Configurer l’environnement virtuel Python

        Créer et activer un environnement virtuel :
            python -m venv venv
            .\venv\Scripts\activate


        Installer les dépendances Python :pip install -r requirements.txt


3. Configurer MySQL

        Accéder à MySQL : mysql -u root -p


        Créer la base de données projet_al : CREATE DATABASE projet_al;


        Configurer l’utilisateur root (avec le mot de passe wtxLUd69i) :
        ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'wtxLUd68i';
        FLUSH PRIVILEGES;


        Importer le schéma et les données initiales :
        mysql -u root -p projet_al < backend/database/schema.sql
        mysql -u root -p projet_al < backend/database/seed.sql


4. Configurer le frontend (Tailwind CSS)

        Naviguer dans le dossier frontend/public : cd frontend\public


        Initialiser un projet Node.js (si nécessaire) : npm init -y


        Installer Tailwind CSS : npm install -D tailwindcss@3.4.3


        Générer css/output.css : npx tailwindcss -i ./css/input.css -o ./css/output.css --minify



## Exécution
1. Lancer le service REST

        Naviguer dans le dossier du service REST :cd backend\rest_service\src

        Lancer le serveur Flask : python main.py


2. Lancer le service SOAP

        Naviguer dans le dossier du service SOAP : cd backend\soap_service\src

        Lancer le serveur SOAP : python main.py


3. Lancer le client SOAP

        Naviguer dans le dossier du client : cd client_app\src

        Exécuter le client : python main.py



4. Lancer le frontend

        Naviguer dans le dossier frontend/public : cd frontend\public

        Lancer le serveur HTTP : python -m http.server 8000


On pourra ouvir dans un navigateur :
- http://localhost:8000/index.html (interface pour visiteurs).
- http://localhost:8000/login.html (connexion pour éditeurs/administrateurs).
- http://localhost:8000/gestion_categories.html (gestion des catégories, pour administrateurs).
- http://localhost:8000/gestion_articles.html (gestion des articles, pour éditeurs/administrateurs).
- http://localhost:8000/gestion_utilisateurs.html (gestion des utilisateurs, pour administrateurs).
- http://localhost:8000/dashboard.html (tableau de bord administrateur).



## Fonctionnalités

**Visiteurs (non connectés)** :
- Consultation des articles sur index.html.
- Filtrage par catégorie via
- Détails des articles dans une modale 



**Éditeurs (rôle : editeur)** :
- Authentification via login.html.
- Redirection vers gestion_articles.html après connexion.
- Gestion des articles (ajouter, modifier, supprimer) avec un tableau (ID, Titre, Résumé, Catégorie,Actions).
- Gestion des catégories via gestion_categories.html (ajouter, modifier, supprimer).


**Administrateurs (rôle : administrateur)** :
- Redirection vers dashboard.html après connexion.
- Gestion des articles via gestion_articles.html (comme les éditeurs).
- Gestion des utilisateurs via gestion_utilisateurs.html (lister, ajouter, modifier, supprimer).
- Gestion des catégories via gestion_categories.html.


## Fin 