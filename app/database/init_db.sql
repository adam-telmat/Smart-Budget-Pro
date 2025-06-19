-- Script d'initialisation de la base de données Smart Budget Pro
-- Crée les tables et insère des données de test

-- Création de la table utilisateurs
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    nom TEXT NOT NULL,
    prenom TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hashed TEXT NOT NULL
);

-- Création de la table transactions
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    reference TEXT NOT NULL,
    description TEXT,
    montant REAL NOT NULL,
    date TEXT NOT NULL,
    type TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

-- Insertion d'un utilisateur de test
-- Mot de passe: Test1234 (haché en SHA-256)
INSERT OR IGNORE INTO users (nom, prenom, email, password_hashed)
VALUES ('Dupont', 'Jean', 'jean.dupont@example.com', '0a041b9462caa4a31bac3567e0b6e6fd9100787db2ab433d96f6d178cabfce90');

-- Insertion de transactions de test pour l'utilisateur
INSERT OR IGNORE INTO transactions (user_id, reference, description, montant, date, type)
VALUES 
    (1, 'REV001', 'Vente de produits', 5000.00, '2023-01-15', 'revenu'),
    (1, 'DEP001', 'Achat fournitures', 1200.50, '2023-01-20', 'dépense'),
    (1, 'REV002', 'Prestation de service', 3500.00, '2023-02-05', 'revenu'),
    (1, 'DEP002', 'Loyer bureau', 800.00, '2023-02-10', 'dépense'),
    (1, 'REV003', 'Vente de produits', 4800.00, '2023-03-12', 'revenu'),
    (1, 'DEP003', 'Facture électricité', 150.75, '2023-03-15', 'dépense'),
    (1, 'REV004', 'Contrat annuel', 12000.00, '2023-04-01', 'revenu'),
    (1, 'DEP004', 'Salaires', 3500.00, '2023-04-05', 'dépense'),
    (1, 'REV005', 'Vente de produits', 6200.00, '2023-05-10', 'revenu'),
    (1, 'DEP005', 'Marketing', 1800.00, '2023-05-15', 'dépense'); 