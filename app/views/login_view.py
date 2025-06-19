#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Smart Budget Pro - Vue de connexion

import tkinter as tk
from tkinter import messagebox
import re

from app.database.db_manager import DatabaseManager
from app.views.register_view import RegisterView
from app.views.dashboard_view import DashboardView

class LoginView:
    """Classe gérant l'interface de connexion"""
    
    def __init__(self, master):
        """
        Initialise la vue de connexion
        
        Args:
            master: Fenêtre Tkinter principale
        """
        self.master = master
        self.db_manager = DatabaseManager()
        
        # Initialisation de la base de données
        self.db_manager.initialize_database()
        
        # Création du cadre principal
        self.frame = tk.Frame(self.master, padx=20, pady=20)
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        # Titre de la page
        title_label = tk.Label(self.frame, text="Smart Budget Pro", font=("Arial", 18, "bold"))
        title_label.pack(pady=20)
        
        subtitle_label = tk.Label(self.frame, text="Connexion", font=("Arial", 14))
        subtitle_label.pack(pady=10)
        
        # Formulaire de connexion
        form_frame = tk.Frame(self.frame)
        form_frame.pack(pady=20)
        
        # Email
        email_label = tk.Label(form_frame, text="Email:", font=("Arial", 12))
        email_label.grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.email_entry = tk.Entry(form_frame, width=30, font=("Arial", 12))
        self.email_entry.grid(row=0, column=1, pady=5, padx=10)
        
        # Mot de passe
        password_label = tk.Label(form_frame, text="Mot de passe:", font=("Arial", 12))
        password_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.password_entry = tk.Entry(form_frame, width=30, font=("Arial", 12), show="*")
        self.password_entry.grid(row=1, column=1, pady=5, padx=10)
        
        # Bouton de connexion
        btn_frame = tk.Frame(self.frame)
        btn_frame.pack(pady=10)
        
        login_button = tk.Button(btn_frame, text="Se connecter", 
                                 command=self.login, font=("Arial", 12),
                                 bg="#4CAF50", fg="white", padx=10, pady=5)
        login_button.pack(side=tk.LEFT, padx=10)
        
        register_button = tk.Button(btn_frame, text="S'inscrire", 
                                   command=self.open_register, font=("Arial", 12),
                                   bg="#2196F3", fg="white", padx=10, pady=5)
        register_button.pack(side=tk.LEFT, padx=10)
    
    def validate_email(self, email):
        """Valide le format de l'email"""
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return re.match(pattern, email) is not None
    
    def login(self):
        """Gère le processus de connexion"""
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        
        # Validation des champs
        if not email or not password:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs")
            return
        
        if not self.validate_email(email):
            messagebox.showerror("Erreur", "Format d'email invalide")
            return
        
        # Tentative d'authentification
        user = self.db_manager.authenticate_user(email, password)
        
        if user:
            # Connexion réussie
            self.open_dashboard(user)
        else:
            messagebox.showerror("Erreur", "Email ou mot de passe incorrect")
    
    def open_register(self):
        """Ouvre la vue d'inscription"""
        self.frame.destroy()
        RegisterView(self.master)
    
    def open_dashboard(self, user):
        """
        Ouvre le tableau de bord après connexion réussie
        
        Args:
            user: Dictionnaire contenant les informations de l'utilisateur
        """
        self.frame.destroy()
        DashboardView(self.master, user) 