-- Données initiales pour la base de données 

-- backend/database/seed.sql
INSERT INTO categories (name) VALUES
    ('Culture'),
    ('Économie'),
    ('Éducation'),
    ('Environnement'),
    ('Politique'),
    ('Santé'),
    ('Sciences'),
    ('Sport'),
    ('Technologie'),
    ('Voyage');

INSERT INTO articles (title, summary, category_id) VALUES
    ('Football : Coupe du Monde 2026', 'Préparatifs pour la prochaine Coupe du Monde.', 8),
    ('Élections 2025 : Analyse', 'Résultats des élections récentes.', 5),
    ('Nouvelles avancées en IA', 'Découvertes en intelligence artificielle.', 9),
    ('Changement climatique : Solutions', 'Stratégies pour réduire les émissions.', 4);

INSERT INTO users (username, password, role) VALUES
    ('editor1', 'password123', 'editor'),
    ('admin1', 'password123', 'admin');