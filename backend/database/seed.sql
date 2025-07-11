-- Données initiales pour la base de données 

-- backend/database/seed.sql
INSERT INTO users (username, password, role) VALUES
    ('admin1', 'hashed_password', 'admin'),
    ('editor1', 'hashed_password', 'editor'),
    ('visitor1', 'hashed_password', 'visitor');

INSERT INTO categories (name) VALUES
    ('News'),
    ('Tech');

INSERT INTO articles (title, summary, content, category_id) VALUES
    ('Article 1', 'Résumé de l''article 1', 'Contenu complet de l''article 1', 1),
    ('Article 2', 'Résumé de l''article 2', 'Contenu complet de l''article 2', 2);
