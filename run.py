#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Smart Budget Pro - Outil de gestion financière pour PME
Développé par Adam - La Plateforme (Marseille)

Ce script permet de lancer l'application avec une interface graphique complète.
"""

import os
import sys
import time
import importlib
import subprocess
import platform
from pathlib import Path

# Bannière ASCII
BANNER = """
╔═══════════════════════════════════════════════════════════════════════╗
║                                                                       ║
║   ███████╗███╗   ███╗ █████╗ ██████╗ ████████╗                        ║
║   ██╔════╝████╗ ████║██╔══██╗██╔══██╗╚══██╔══╝                        ║
║   ███████╗██╔████╔██║███████║██████╔╝   ██║                           ║
║   ╚════██║██║╚██╔╝██║██╔══██║██╔══██╗   ██║                           ║
║   ███████║██║ ╚═╝ ██║██║  ██║██║  ██║   ██║                           ║
║   ╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝                           ║
║                                                                       ║
║   ██████╗ ██╗   ██╗██████╗  ██████╗ ███████╗████████╗                 ║
║   ██╔══██╗██║   ██║██╔══██╗██╔════╝ ██╔════╝╚══██╔══╝                 ║
║   ██████╔╝██║   ██║██║  ██║██║  ███╗█████╗     ██║                    ║
║   ██╔══██╗██║   ██║██║  ██║██║   ██║██╔══╝     ██║                    ║
║   ██████╔╝╚██████╔╝██████╔╝╚██████╔╝███████╗   ██║                    ║
║   ╚═════╝  ╚═════╝ ╚═════╝  ╚═════╝ ╚══════╝   ╚═╝                    ║
║                                                                       ║
║   ██████╗ ██████╗  ██████╗                                            ║
║   ██╔══██╗██╔══██╗██╔═══██╗                                           ║
║   ██████╔╝██████╔╝██║   ██║                                           ║
║   ██╔═══╝ ██╔══██╗██║   ██║                                           ║
║   ██║     ██║  ██║╚██████╔╝                                           ║
║   ╚═╝     ╚═╝  ╚═╝ ╚═════╝                                            ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
                                    v1.0.0

    Outil financier pour PME: gestion des finances, prédictions IA
    et visualisations interactives. Développé avec Python et SQLite.
"""

# Liste des dépendances requises avec leurs versions minimales
REQUIRED_PACKAGES = {
    "pandas": "1.0.0",
    "numpy": "1.18.0",
    "matplotlib": "3.1.0",
    "sklearn": "0.22.0"
}

def print_colored(text, color="default"):
    """Affiche du texte coloré dans le terminal"""
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "purple": "\033[95m",
        "cyan": "\033[96m",
        "default": "\033[0m"
    }
    
    # Windows peut avoir des problèmes avec les codes ANSI
    if platform.system() == "Windows":
        try:
            # Activer le support ANSI pour Windows 10+
            import ctypes
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        except:
            # Si ça échoue, imprimer sans couleur
            print(text)
            return
    
    end_color = colors["default"]
    color_code = colors.get(color, end_color)
    print(f"{color_code}{text}{end_color}")

def clear_screen():
    """Nettoie l'écran du terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def check_dependencies():
    """Vérifie si toutes les dépendances sont installées avec les versions minimales requises"""
    print_colored("\nVérification des dépendances requises...", "blue")
    missing_packages = []
    
    for package, min_version in REQUIRED_PACKAGES.items():
        try:
            imported = importlib.import_module(package.replace("-", "_"))
            version = imported.__version__
            print_colored(f"✓ {package} v{version}", "green")
        except ImportError:
            missing_packages.append(package)
            print_colored(f"✗ {package} - Non installé", "red")
    
    # Afficher un avertissement pour les packages manquants
    if missing_packages:
        print_colored("\nAttention: Certaines dépendances sont manquantes.", "yellow")
        packages_str = " ".join(missing_packages)
        install_cmd = f"pip install {packages_str}"
        print(f"  {install_cmd}")
        
        choice = input("\nVoulez-vous installer ces packages maintenant? (o/n): ")
        
        if choice.lower() == 'o':
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing_packages)
                print_colored("\nDépendances installées avec succès!", "green")
                time.sleep(1)
            except subprocess.CalledProcessError:
                print_colored("\nErreur lors de l'installation des dépendances.", "red")
                print_colored("Veuillez les installer manuellement avec pip.", "red")
                choice = input("\nVoulez-vous continuer quand même? (o/n): ")
                if choice.lower() != 'o':
                    sys.exit(1)
        else:
            choice = input("\nVoulez-vous continuer sans installer les dépendances? (o/n): ")
            if choice.lower() != 'o':
                sys.exit(1)
    else:
        print_colored("\nToutes les dépendances sont correctement installées!", "green")
        time.sleep(1)

def initialize_test_data():
    """Initialise les données de test dans la base de données"""
    print_colored("\nInitialisation des données de test...", "blue")
    try:
        from app.database.db_manager import DatabaseManager
        db_manager = DatabaseManager()
        db_manager.initialize_database()
        
        # Vérifier si l'utilisateur de test existe déjà
        existing_user = db_manager.authenticate_user("jean.dupont@example.com", "Test1234")
        if not existing_user:
            # Créer l'utilisateur de test
            success = db_manager.register_user("Dupont", "Jean", "jean.dupont@example.com", "Test1234")
            if success:
                print_colored("✓ Utilisateur de test créé", "green")
                
                # Ajouter quelques transactions de test
                user = db_manager.authenticate_user("jean.dupont@example.com", "Test1234")
                if user:
                    user_id = user['id']
                    # Transactions de test sur différents mois
                    test_transactions = [
                        (user_id, "REV001", "Vente de produits", 5000.00, "2023-01-15", "revenu"),
                        (user_id, "DEP001", "Achat fournitures", 1200.50, "2023-01-20", "dépense"),
                        (user_id, "REV002", "Prestation de service", 3500.00, "2023-02-05", "revenu"),
                        (user_id, "DEP002", "Loyer bureau", 800.00, "2023-02-10", "dépense"),
                        (user_id, "REV003", "Vente de produits", 4800.00, "2023-03-12", "revenu"),
                        (user_id, "DEP003", "Facture électricité", 150.75, "2023-03-15", "dépense"),
                    ]
                    
                    for transaction in test_transactions:
                        db_manager.add_transaction(*transaction)
                    
                    print_colored("✓ Transactions de test ajoutées", "green")
            else:
                print_colored("⚠ Erreur lors de la création de l'utilisateur de test", "yellow")
        else:
            print_colored("✓ Utilisateur de test déjà existant", "green")
            
    except Exception as e:
        print_colored(f"⚠ Erreur lors de l'initialisation: {e}", "yellow")

def main():
    """Fonction principale qui lance l'application"""
    # Ajouter le répertoire racine au PYTHONPATH
    project_root = Path(__file__).resolve().parent
    sys.path.insert(0, str(project_root))
    
    try:
        # Vider l'écran et afficher la bannière
        clear_screen()
        print_colored(BANNER, "cyan")
        
        # Vérifier les dépendances
        check_dependencies()
        
        # Initialiser les données de test
        initialize_test_data()
        
        print_colored("\nDémarrage de Smart Budget Pro...", "blue")
        
        # Petit délai pour l'effet visuel
        time.sleep(1)
        
        # Informations de connexion utiles pour la démo
        print_colored("\nIdentifiants de démonstration:", "yellow")
        print_colored("  Email: jean.dupont@example.com", "yellow")
        print_colored("  Mot de passe: Test1234", "yellow")
        print_colored("\nAppuyez sur Entrée pour continuer...", "green")
        input()
        
        # Importer et lancer l'application
        from app.main import main
        main()
        
    except ImportError as e:
        print_colored(f"\nErreur lors de l'importation des modules: {e}", "red")
        print_colored("\nAssurez-vous que la structure du projet est correcte:", "red")
        print_colored("  app/", "default")
        print_colored("  ├── __init__.py", "default")
        print_colored("  ├── main.py", "default")
        print_colored("  ├── config/", "default")
        print_colored("  ├── database/", "default")
        print_colored("  ├── models/", "default")
        print_colored("  └── views/", "default")
        sys.exit(1)
        
    except Exception as e:
        print_colored(f"\nUne erreur inattendue est survenue: {e}", "red")
        print_colored("Veuillez vérifier les logs pour plus de détails.", "red")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main() 