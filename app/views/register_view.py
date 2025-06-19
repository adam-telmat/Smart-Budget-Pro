#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Smart Budget Pro - Vue d'inscription

import tkinter as tk
from tkinter import messagebox
import re

from app.database.db_manager import DatabaseManager
from app.config.settings import PASSWORD_MIN_LENGTH

class RegisterView:
    """Classe gérant l'interface d'inscription"""
    
    def __init__(self, master):
        """
        Initialise la vue d'inscription
        
        Args:
            master: Fenêtre Tkinter principale
        """
        self.master = master
        self.db_manager = DatabaseManager()
        
        # Création du cadre principal
        self.frame = tk.Frame(self.master, padx=20, pady=20)
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        # Titre de la page
        title_label = tk.Label(self.frame, text="Smart Budget Pro", font=("Arial", 18, "bold"))
        title_label.pack(pady=20)
        
        subtitle_label = tk.Label(self.frame, text="Inscription", font=("Arial", 14))
        subtitle_label.pack(pady=10)
        
        # Formulaire d'inscription
        form_frame = tk.Frame(self.frame)
        form_frame.pack(pady=20)
        
        # Nom
        nom_label = tk.Label(form_frame, text="Nom:", font=("Arial", 12))
        nom_label.grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.nom_entry = tk.Entry(form_frame, width=30, font=("Arial", 12))
        self.nom_entry.grid(row=0, column=1, pady=5, padx=10)
        
        # Prénom
        prenom_label = tk.Label(form_frame, text="Prénom:", font=("Arial", 12))
        prenom_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.prenom_entry = tk.Entry(form_frame, width=30, font=("Arial", 12))
        self.prenom_entry.grid(row=1, column=1, pady=5, padx=10)
        
        # Email
        email_label = tk.Label(form_frame, text="Email:", font=("Arial", 12))
        email_label.grid(row=2, column=0, sticky=tk.W, pady=5)
        
        self.email_entry = tk.Entry(form_frame, width=30, font=("Arial", 12))
        self.email_entry.grid(row=2, column=1, pady=5, padx=10)
        
        # Mot de passe
        password_label = tk.Label(form_frame, text="Mot de passe:", font=("Arial", 12))
        password_label.grid(row=3, column=0, sticky=tk.W, pady=5)
        
        self.password_entry = tk.Entry(form_frame, width=30, font=("Arial", 12), show="*")
        self.password_entry.grid(row=3, column=1, pady=5, padx=10)
        
        # Confirmation mot de passe
        confirm_label = tk.Label(form_frame, text="Confirmer:", font=("Arial", 12))
        confirm_label.grid(row=4, column=0, sticky=tk.W, pady=5)
        
        self.confirm_entry = tk.Entry(form_frame, width=30, font=("Arial", 12), show="*")
        self.confirm_entry.grid(row=4, column=1, pady=5, padx=10)
        
        # Informations sur les exigences de mot de passe
        password_info = tk.Label(self.frame, 
                               text=f"Le mot de passe doit contenir au moins {PASSWORD_MIN_LENGTH} caractères, \n"
                                    "une majuscule et un chiffre.",
                               font=("Arial", 10), fg="gray")
        password_info.pack(pady=5)
        
        # Boutons
        btn_frame = tk.Frame(self.frame)
        btn_frame.pack(pady=10)
        
        register_button = tk.Button(btn_frame, text="S'inscrire", 
                                   command=self.register, font=("Arial", 12),
                                   bg="#4CAF50", fg="white", padx=10, pady=5)
        register_button.pack(side=tk.LEFT, padx=10)
        
        back_button = tk.Button(btn_frame, text="Retour", 
                              command=self.back_to_login, font=("Arial", 12),
                              bg="#f44336", fg="white", padx=10, pady=5)
        back_button.pack(side=tk.LEFT, padx=10)
    
    def validate_email(self, email):
        """Valide le format de l'email"""
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return re.match(pattern, email) is not None
    
    def validate_password(self, password):
        """
        Valide la complexité du mot de passe
        Le mot de passe doit contenir au moins 8 caractères, une majuscule et un chiffre
        """
        if len(password) < PASSWORD_MIN_LENGTH:
            return False
        
        if not re.search(r"[A-Z]", password):
            return False
            
        if not re.search(r"\d", password):
            return False
            
        return True
    
    def register(self):
        """Gère le processus d'inscription"""
        nom = self.nom_entry.get().strip()
        prenom = self.prenom_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get()
        confirm = self.confirm_entry.get()
        
        # Validation des champs
        if not all([nom, prenom, email, password, confirm]):
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs")
            return
        
        if not self.validate_email(email):
            messagebox.showerror("Erreur", "Format d'email invalide")
            return
        
        if not self.validate_password(password):
            messagebox.showerror("Erreur", 
                                f"Le mot de passe doit contenir au moins {PASSWORD_MIN_LENGTH} caractères, "
                                "une majuscule et un chiffre")
            return
        
        if password != confirm:
            messagebox.showerror("Erreur", "Les mots de passe ne correspondent pas")
            return
        
        # Tentative d'inscription
        success = self.db_manager.register_user(nom, prenom, email, password)
        
        if success:
            messagebox.showinfo("Succès", "Inscription réussie! Vous pouvez maintenant vous connecter.")
            self.back_to_login()
        else:
            messagebox.showerror("Erreur", "L'inscription a échoué. Cet email est peut-être déjà utilisé.")
    
    def back_to_login(self):
        """Retourne à la page de connexion"""
        self.frame.destroy()
        # Importer ici pour éviter les importations circulaires
        from app.views.login_view import LoginView
        LoginView(self.master) 