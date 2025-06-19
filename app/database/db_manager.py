#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Smart Budget Pro - Gestionnaire de base de données

import sqlite3
import os
from app.config.settings import DB_PATH
import hashlib

class DatabaseManager:
    """Classe gérant les interactions avec la base de données SQLite"""
    
    def __init__(self):
        """Initialise la connexion à la base de données"""
        # Créer le répertoire de la base de données si nécessaire
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        
        self.conn = None
        self.cursor = None
        
    def connect(self):
        """Établit une connexion à la base de données"""
        try:
            self.conn = sqlite3.connect(DB_PATH)
            self.cursor = self.conn.cursor()
            return True
        except sqlite3.Error as e:
            print(f"Erreur de connexion à la base de données: {e}")
            return False
            
    def disconnect(self):
        """Ferme la connexion à la base de données"""
        if self.conn:
            self.conn.close()
            
    def execute_query(self, query, params=()):
        """Exécute une requête SQL avec les paramètres fournis"""
        try:
            self.connect()
            self.cursor.execute(query, params)
            self.conn.commit()
            result = True
        except sqlite3.Error as e:
            print(f"Erreur d'exécution de requête: {e}")
            result = False
        finally:
            self.disconnect()
        return result
            
    def fetch_query(self, query, params=()):
        """Exécute une requête et renvoie les résultats"""
        try:
            self.connect()
            self.cursor.execute(query, params)
            result = self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Erreur de récupération de données: {e}")
            result = []
        finally:
            self.disconnect()
        return result
    
    def initialize_database(self):
        """Initialise la structure de la base de données"""
        # Création de la table utilisateurs
        users_table = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            nom TEXT NOT NULL,
            prenom TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hashed TEXT NOT NULL
        );
        """
        
        # Création de la table transactions
        transactions_table = """
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
        """
        
        # Exécution des requêtes de création
        self.execute_query(users_table)
        self.execute_query(transactions_table)
    
    def hash_password(self, password):
        """Hachage du mot de passe avec SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_user(self, nom, prenom, email, password):
        """Enregistre un nouvel utilisateur dans la base de données"""
        hashed_password = self.hash_password(password)
        query = "INSERT INTO users (nom, prenom, email, password_hashed) VALUES (?, ?, ?, ?)"
        return self.execute_query(query, (nom, prenom, email, hashed_password))
    
    def authenticate_user(self, email, password):
        """Authentifie un utilisateur"""
        hashed_password = self.hash_password(password)
        query = "SELECT id, nom, prenom FROM users WHERE email = ? AND password_hashed = ?"
        result = self.fetch_query(query, (email, hashed_password))
        
        if result:
            user_id, nom, prenom = result[0]
            return {"id": user_id, "nom": nom, "prenom": prenom}
        return None
    
    def add_transaction(self, user_id, reference, description, montant, date, type_):
        """Ajoute une nouvelle transaction pour un utilisateur"""
        query = """
        INSERT INTO transactions (user_id, reference, description, montant, date, type)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        return self.execute_query(query, (user_id, reference, description, montant, date, type_))
    
    def get_transactions(self, user_id, date_from=None, date_to=None):
        """Récupère les transactions d'un utilisateur avec filtrage par date optionnel"""
        if date_from and date_to:
            query = """
            SELECT id, reference, description, montant, date, type 
            FROM transactions 
            WHERE user_id = ? AND date BETWEEN ? AND ?
            ORDER BY date DESC
            """
            return self.fetch_query(query, (user_id, date_from, date_to))
        else:
            query = """
            SELECT id, reference, description, montant, date, type 
            FROM transactions 
            WHERE user_id = ?
            ORDER BY date DESC
            """
            return self.fetch_query(query, (user_id,))
    
    def get_balance(self, user_id):
        """Calcule le solde total pour un utilisateur"""
        query = """
        SELECT SUM(CASE WHEN type = 'revenu' THEN montant 
                        WHEN type = 'dépense' THEN -montant
                        ELSE 0 END) 
        FROM transactions 
        WHERE user_id = ?
        """
        result = self.fetch_query(query, (user_id,))
        if result and result[0][0]:
            return result[0][0]
        return 0 