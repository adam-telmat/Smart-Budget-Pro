#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Smart Budget Pro - Outil de gestion financière pour PME
# Par Adam - La Plateforme (Marseille)

import tkinter as tk

from app.views.login_view import LoginView
from app.config.settings import APP_TITLE, APP_SIZE

def main():
    """Point d'entrée principal de l'application Smart Budget Pro"""
    # Initialisation de la fenêtre principale
    root = tk.Tk()
    root.title(APP_TITLE)
    root.geometry(APP_SIZE)
    root.resizable(False, False)
    
    # Lancement de l'application avec la vue de connexion
    app = LoginView(root)
    root.mainloop()

if __name__ == "__main__":
    main() 