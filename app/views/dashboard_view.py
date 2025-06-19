#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Smart Budget Pro - Vue du tableau de bord

import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta
import pandas as pd

from app.database.db_manager import DatabaseManager
from app.models.prediction_model import PredictionModel
from app.config.settings import DATE_FORMAT

class DashboardView:
    """Classe gérant l'interface du tableau de bord principal"""
    
    def __init__(self, master, user):
        """
        Initialise la vue du tableau de bord
        
        Args:
            master: Fenêtre Tkinter principale
            user: Dictionnaire contenant les informations de l'utilisateur
        """
        self.master = master
        self.user = user
        self.db_manager = DatabaseManager()
        
        # Création du cadre principal
        self.frame = tk.Frame(self.master)
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        # En-tête avec informations utilisateur
        self._create_header()
        
        # Création des onglets
        self.tab_control = ttk.Notebook(self.frame)
        
        # Onglet Vue générale
        self.overview_tab = tk.Frame(self.tab_control)
        self.tab_control.add(self.overview_tab, text="Vue générale")
        
        # Onglet Transactions
        self.transactions_tab = tk.Frame(self.tab_control)
        self.tab_control.add(self.transactions_tab, text="Transactions")
        
        # Onglet Prédictions
        self.predictions_tab = tk.Frame(self.tab_control)
        self.tab_control.add(self.predictions_tab, text="Prédictions")
        
        self.tab_control.pack(expand=1, fill=tk.BOTH, padx=10, pady=5)
        
        # Configuration des onglets
        self._setup_overview_tab()
        self._setup_transactions_tab()
        self._setup_predictions_tab()
        
        # Liaison des événements de changement d'onglet
        self.tab_control.bind("<<NotebookTabChanged>>", self._on_tab_change)
    
    def _create_header(self):
        """Crée l'en-tête du tableau de bord avec les informations utilisateur"""
        header_frame = tk.Frame(self.frame, bg="#f0f0f0", padx=10, pady=5)
        header_frame.pack(fill=tk.X)
        
        # Titre de l'application
        title_label = tk.Label(header_frame, text="Smart Budget Pro", 
                             font=("Arial", 16, "bold"), bg="#f0f0f0")
        title_label.pack(side=tk.LEFT, padx=10)
        
        # Informations utilisateur
        user_info = f"{self.user['prenom']} {self.user['nom']}"
        user_label = tk.Label(header_frame, text=user_info, 
                            font=("Arial", 12), bg="#f0f0f0")
        user_label.pack(side=tk.RIGHT, padx=10)
        
        # Bouton de déconnexion
        logout_button = tk.Button(header_frame, text="Déconnexion", 
                                command=self._logout, bg="#f44336", fg="white")
        logout_button.pack(side=tk.RIGHT, padx=5)
    
    def _setup_overview_tab(self):
        """Configure l'onglet Vue générale"""
        # Cadre supérieur pour le solde
        top_frame = tk.Frame(self.overview_tab, padx=20, pady=10)
        top_frame.pack(fill=tk.X)
        
        # Solde actuel
        balance_frame = tk.LabelFrame(top_frame, text="Solde actuel", padx=10, pady=10)
        balance_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.balance_label = tk.Label(balance_frame, text="0 €", font=("Arial", 24, "bold"))
        self.balance_label.pack(pady=10)
        
        # Boutons d'actions rapides
        actions_frame = tk.LabelFrame(top_frame, text="Actions rapides", padx=10, pady=10)
        actions_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        add_transaction_btn = tk.Button(actions_frame, text="Nouvelle transaction", 
                                      command=lambda: self.tab_control.select(1))
        add_transaction_btn.pack(fill=tk.X, pady=5)
        
        predict_btn = tk.Button(actions_frame, text="Voir prédictions", 
                              command=lambda: self.tab_control.select(2))
        predict_btn.pack(fill=tk.X, pady=5)
        
        export_btn = tk.Button(actions_frame, text="Exporter données", 
                             command=self._export_data)
        export_btn.pack(fill=tk.X, pady=5)
        
        # Cadre pour le graphique
        self.chart_frame = tk.LabelFrame(self.overview_tab, text="Revenus vs Dépenses", padx=10, pady=10)
        self.chart_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Le graphique sera créé lors de l'actualisation des données
        
        # Chargement initial des données
        self._update_overview()
    
    def _setup_transactions_tab(self):
        """Configure l'onglet Transactions"""
        # Cadre supérieur pour les filtres et la saisie
        top_frame = tk.Frame(self.transactions_tab, padx=20, pady=10)
        top_frame.pack(fill=tk.X)
        
        # Filtres de recherche
        filter_frame = tk.LabelFrame(top_frame, text="Filtrer par date", padx=10, pady=10)
        filter_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        tk.Label(filter_frame, text="Du:").grid(row=0, column=0, padx=5, pady=5)
        self.date_from_entry = tk.Entry(filter_frame, width=12)
        self.date_from_entry.grid(row=0, column=1, padx=5, pady=5)
        self.date_from_entry.insert(0, (datetime.now() - timedelta(days=30)).strftime(DATE_FORMAT))
        
        tk.Label(filter_frame, text="Au:").grid(row=0, column=2, padx=5, pady=5)
        self.date_to_entry = tk.Entry(filter_frame, width=12)
        self.date_to_entry.grid(row=0, column=3, padx=5, pady=5)
        self.date_to_entry.insert(0, datetime.now().strftime(DATE_FORMAT))
        
        search_btn = tk.Button(filter_frame, text="Rechercher", command=self._filter_transactions)
        search_btn.grid(row=0, column=4, padx=10, pady=5)
        
        # Bouton pour ajouter une transaction
        add_btn = tk.Button(top_frame, text="Nouvelle transaction", 
                          command=self._open_add_transaction, bg="#4CAF50", fg="white")
        add_btn.pack(side=tk.RIGHT, padx=20, pady=10)
        
        # Tableau des transactions
        table_frame = tk.Frame(self.transactions_tab, padx=20, pady=10)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Création du treeview pour les transactions
        columns = ("ID", "Référence", "Description", "Montant", "Date", "Type")
        self.transactions_tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        # Configuration des colonnes
        self.transactions_tree.heading("ID", text="ID")
        self.transactions_tree.heading("Référence", text="Référence")
        self.transactions_tree.heading("Description", text="Description")
        self.transactions_tree.heading("Montant", text="Montant")
        self.transactions_tree.heading("Date", text="Date")
        self.transactions_tree.heading("Type", text="Type")
        
        # Ajustement des largeurs
        self.transactions_tree.column("ID", width=50)
        self.transactions_tree.column("Référence", width=100)
        self.transactions_tree.column("Description", width=200)
        self.transactions_tree.column("Montant", width=100)
        self.transactions_tree.column("Date", width=100)
        self.transactions_tree.column("Type", width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.transactions_tree.yview)
        self.transactions_tree.configure(yscroll=scrollbar.set)
        
        # Placement du tableau et de la scrollbar
        self.transactions_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Chargement initial des transactions
        self._load_transactions()
    
    def _setup_predictions_tab(self):
        """Configure l'onglet Prédictions"""
        # Cadre supérieur avec informations
        info_frame = tk.Frame(self.predictions_tab, padx=20, pady=10)
        info_frame.pack(fill=tk.X)
        
        info_label = tk.Label(info_frame, 
                             text="Prédictions basées sur l'historique de vos transactions",
                             font=("Arial", 12))
        info_label.pack(pady=10)
        
        # Cadre pour le statut des prédictions
        status_frame = tk.Frame(self.predictions_tab, padx=20, pady=5)
        status_frame.pack(fill=tk.X)
        
        self.prediction_status = tk.Label(status_frame, text="", font=("Arial", 11))
        self.prediction_status.pack(side=tk.LEFT, pady=5)
        
        # Boutons de contrôle
        predict_btn = tk.Button(status_frame, text="Générer prédictions", 
                              command=self._generate_predictions)
        predict_btn.pack(side=tk.RIGHT, padx=5)
        
        compare_btn = tk.Button(status_frame, text="Comparer modèles", 
                              command=self._compare_models)
        compare_btn.pack(side=tk.RIGHT, padx=5)
        
        # Cadre pour les graphiques
        self.prediction_frame = tk.LabelFrame(self.predictions_tab, text="Tendances prédites", 
                                            padx=10, pady=10)
        self.prediction_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Cadre pour la recommandation
        self.recommendation_frame = tk.LabelFrame(self.predictions_tab, text="Recommandation", 
                                                padx=10, pady=10)
        self.recommendation_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.recommendation_label = tk.Label(self.recommendation_frame, 
                                          text="Générez des prédictions pour obtenir des recommandations",
                                          font=("Arial", 12))
        self.recommendation_label.pack(pady=10)
    
    def _logout(self):
        """Déconnecte l'utilisateur et retourne à l'écran de connexion"""
        self.frame.destroy()
        # Importer ici pour éviter les importations circulaires
        from app.views.login_view import LoginView
        LoginView(self.master)
    
    def _update_overview(self):
        """Met à jour les données de la vue générale"""
        # Mise à jour du solde
        balance = self.db_manager.get_balance(self.user['id'])
        self.balance_label.config(text=f"{balance:.2f} €")
        
        # Récupération des transactions pour le graphique
        transactions = self.db_manager.get_transactions(self.user['id'])
        
        # Si aucune transaction, afficher un message
        if not transactions:
            if hasattr(self, 'canvas'):
                self.canvas.get_tk_widget().destroy()
            
            no_data_label = tk.Label(self.chart_frame, 
                                   text="Aucune donnée disponible.\nAjoutez des transactions pour voir le graphique.",
                                   font=("Arial", 12))
            no_data_label.pack(pady=50)
            return
        
        # Préparation des données pour le graphique
        df = pd.DataFrame(transactions, 
                         columns=['id', 'reference', 'description', 'montant', 'date', 'type'])
        
        # Conversion des dates
        df['date'] = pd.to_datetime(df['date'])
        df['mois'] = df['date'].dt.strftime('%Y-%m')
        
        # Calcul des revenus et dépenses par mois
        income_by_month = df[df['type'] == 'revenu'].groupby('mois')['montant'].sum()
        expense_by_month = df[df['type'] == 'dépense'].groupby('mois')['montant'].sum()
        
        # Création du graphique
        fig, ax = plt.subplots(figsize=(8, 4))
        
        months = list(set(income_by_month.index) | set(expense_by_month.index))
        months.sort()
        
        income_values = [income_by_month.get(month, 0) for month in months]
        expense_values = [expense_by_month.get(month, 0) for month in months]
        
        ax.bar(months, income_values, label='Revenus', color='green', alpha=0.7)
        ax.bar(months, expense_values, label='Dépenses', color='red', alpha=0.7)
        
        ax.set_title('Revenus et Dépenses par Mois')
        ax.set_xlabel('Mois')
        ax.set_ylabel('Montant (€)')
        plt.xticks(rotation=45)
        ax.legend()
        
        plt.tight_layout()
        
        # Suppression de l'ancien graphique s'il existe
        if hasattr(self, 'canvas'):
            self.canvas.get_tk_widget().destroy()
        
        # Affichage du nouveau graphique
        self.canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def _load_transactions(self):
        """Charge les transactions dans le tableau"""
        # Effacer les données existantes
        for item in self.transactions_tree.get_children():
            self.transactions_tree.delete(item)
        
        # Récupérer les transactions filtrées
        date_from = self.date_from_entry.get().strip()
        date_to = self.date_to_entry.get().strip()
        
        if date_from and date_to:
            transactions = self.db_manager.get_transactions(self.user['id'], date_from, date_to)
        else:
            transactions = self.db_manager.get_transactions(self.user['id'])
        
        # Insertion des transactions dans le tableau
        for transaction in transactions:
            transaction_id, reference, description, montant, date, type_ = transaction
            self.transactions_tree.insert('', tk.END, values=(transaction_id, reference, description, 
                                                             f"{montant:.2f} €", date, type_))
    
    def _filter_transactions(self):
        """Filtre les transactions selon les dates entrées"""
        # Validation du format des dates
        date_from = self.date_from_entry.get().strip()
        date_to = self.date_to_entry.get().strip()
        
        try:
            if date_from:
                datetime.strptime(date_from, DATE_FORMAT)
            if date_to:
                datetime.strptime(date_to, DATE_FORMAT)
        except ValueError:
            messagebox.showerror("Erreur", f"Format de date invalide. Utilisez le format {DATE_FORMAT}")
            return
        
        # Rechargement des transactions
        self._load_transactions()
    
    def _open_add_transaction(self):
        """Ouvre la fenêtre d'ajout de transaction"""
        # Création d'une fenêtre modale
        self.add_window = tk.Toplevel(self.master)
        self.add_window.title("Nouvelle transaction")
        self.add_window.geometry("400x350")
        self.add_window.transient(self.master)
        self.add_window.grab_set()
        
        # Cadre du formulaire
        form_frame = tk.Frame(self.add_window, padx=20, pady=20)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Champs du formulaire
        tk.Label(form_frame, text="Référence:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.ref_entry = tk.Entry(form_frame, width=30)
        self.ref_entry.grid(row=0, column=1, pady=5, padx=5)
        
        tk.Label(form_frame, text="Description:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.desc_entry = tk.Entry(form_frame, width=30)
        self.desc_entry.grid(row=1, column=1, pady=5, padx=5)
        
        tk.Label(form_frame, text="Montant (€):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.amount_entry = tk.Entry(form_frame, width=30)
        self.amount_entry.grid(row=2, column=1, pady=5, padx=5)
        
        tk.Label(form_frame, text="Date:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.date_entry = tk.Entry(form_frame, width=30)
        self.date_entry.grid(row=3, column=1, pady=5, padx=5)
        self.date_entry.insert(0, datetime.now().strftime(DATE_FORMAT))
        
        tk.Label(form_frame, text="Type:").grid(row=4, column=0, sticky=tk.W, pady=5)
        
        # Options pour le type
        self.transaction_type = tk.StringVar(value="revenu")
        types_frame = tk.Frame(form_frame)
        types_frame.grid(row=4, column=1, sticky=tk.W, pady=5)
        
        tk.Radiobutton(types_frame, text="Revenu", variable=self.transaction_type, 
                      value="revenu").pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(types_frame, text="Dépense", variable=self.transaction_type, 
                      value="dépense").pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(types_frame, text="Transfert", variable=self.transaction_type, 
                      value="transfert").pack(side=tk.LEFT, padx=5)
        
        # Boutons
        btn_frame = tk.Frame(form_frame)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=15)
        
        save_btn = tk.Button(btn_frame, text="Enregistrer", 
                           command=self._save_transaction, bg="#4CAF50", fg="white")
        save_btn.pack(side=tk.LEFT, padx=10)
        
        cancel_btn = tk.Button(btn_frame, text="Annuler", 
                             command=self.add_window.destroy, bg="#f44336", fg="white")
        cancel_btn.pack(side=tk.LEFT, padx=10)
    
    def _save_transaction(self):
        """Enregistre une nouvelle transaction"""
        # Récupération des valeurs
        reference = self.ref_entry.get().strip()
        description = self.desc_entry.get().strip()
        montant_str = self.amount_entry.get().strip()
        date = self.date_entry.get().strip()
        type_ = self.transaction_type.get()
        
        # Validation des champs
        if not reference:
            messagebox.showerror("Erreur", "La référence est obligatoire")
            return
        
        try:
            montant = float(montant_str)
            if montant <= 0:
                raise ValueError("Le montant doit être positif")
        except ValueError:
            messagebox.showerror("Erreur", "Montant invalide")
            return
        
        try:
            datetime.strptime(date, DATE_FORMAT)
        except ValueError:
            messagebox.showerror("Erreur", f"Format de date invalide. Utilisez le format {DATE_FORMAT}")
            return
        
        # Enregistrement de la transaction
        success = self.db_manager.add_transaction(
            self.user['id'], reference, description, montant, date, type_
        )
        
        if success:
            messagebox.showinfo("Succès", "Transaction enregistrée avec succès")
            self.add_window.destroy()
            
            # Mise à jour des données
            self._load_transactions()
            self._update_overview()
        else:
            messagebox.showerror("Erreur", "Échec de l'enregistrement de la transaction")
    
    def _generate_predictions(self):
        """Génère les prédictions financières"""
        # Récupération des transactions
        transactions = self.db_manager.get_transactions(self.user['id'])
        
        if not transactions or len(transactions) < 3:
            self.prediction_status.config(
                text="Pas assez de données pour générer des prédictions (min. 3 transactions)",
                fg="red"
            )
            return
        
        # Initialisation du modèle de prédiction
        prediction_model = PredictionModel(transactions)
        
        # Génération des prédictions
        predictions_df, r2_score, recommendation = prediction_model.predict_linear_regression()
        
        if len(predictions_df) == 0:
            self.prediction_status.config(
                text="Impossible de générer des prédictions avec les données actuelles",
                fg="red"
            )
            return
        
        # Affichage du statut
        self.prediction_status.config(
            text=f"Prédictions générées (précision R²: {r2_score:.2f})",
            fg="green"
        )
        
        # Affichage de la recommandation
        self.recommendation_label.config(text=recommendation)
        
        # Nettoyage du cadre de prédiction
        for widget in self.prediction_frame.winfo_children():
            widget.destroy()
        
        # Création du graphique de prédiction
        fig, ax = plt.subplots(figsize=(8, 4))
        
        ax.plot(predictions_df['mois'], predictions_df['revenu_predit'], 
               label='Revenus prédits', marker='o', color='green')
        ax.plot(predictions_df['mois'], predictions_df['dépense_predite'], 
               label='Dépenses prédites', marker='o', color='red')
        
        ax.set_title('Prédictions pour les prochains mois')
        ax.set_xlabel('Mois')
        ax.set_ylabel('Montant (€)')
        plt.xticks(rotation=45)
        ax.legend()
        
        plt.tight_layout()
        
        # Affichage du graphique
        canvas = FigureCanvasTkAgg(fig, master=self.prediction_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Si le solde prédit est négatif, afficher une alerte
        if any(predictions_df['solde_predit'] < 0):
            messagebox.showwarning(
                "Alerte", 
                "Attention: Certains mois à venir présentent un solde négatif prédit."
            )
    
    def _compare_models(self):
        """Compare les performances des modèles de prédiction"""
        # Récupération des transactions
        transactions = self.db_manager.get_transactions(self.user['id'])
        
        if not transactions or len(transactions) < 3:
            messagebox.showinfo(
                "Information", 
                "Pas assez de données pour comparer les modèles (min. 3 transactions)"
            )
            return
        
        # Initialisation du modèle de prédiction
        prediction_model = PredictionModel(transactions)
        
        # Génération des prédictions avec les deux modèles
        linear_df, linear_r2, _ = prediction_model.predict_linear_regression()
        forest_df, forest_r2, _ = prediction_model.predict_random_forest()
        
        if len(linear_df) == 0 or len(forest_df) == 0:
            messagebox.showinfo(
                "Information", 
                "Impossible de comparer les modèles avec les données actuelles"
            )
            return
        
        # Affichage des résultats de comparaison
        comparison_window = tk.Toplevel(self.master)
        comparison_window.title("Comparaison des modèles")
        comparison_window.geometry("500x400")
        comparison_window.transient(self.master)
        
        # Cadre principal
        main_frame = tk.Frame(comparison_window, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Titre
        tk.Label(main_frame, text="Comparaison des modèles de prédiction", 
               font=("Arial", 14, "bold")).pack(pady=10)
        
        # Affichage des scores R²
        scores_frame = tk.Frame(main_frame)
        scores_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(scores_frame, text="Précision du modèle (R²):", font=("Arial", 12)).grid(
            row=0, column=0, sticky=tk.W, pady=5)
        
        tk.Label(scores_frame, text=f"Régression linéaire: {linear_r2:.4f}", 
               font=("Arial", 12)).grid(row=1, column=0, sticky=tk.W, pady=5)
        
        tk.Label(scores_frame, text=f"Random Forest: {forest_r2:.4f}", 
               font=("Arial", 12)).grid(row=2, column=0, sticky=tk.W, pady=5)
        
        # Recommandation du meilleur modèle
        best_model = "Régression linéaire" if linear_r2 >= forest_r2 else "Random Forest"
        
        recommendation_frame = tk.LabelFrame(main_frame, text="Recommandation", padx=10, pady=10)
        recommendation_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(recommendation_frame, 
               text=f"Pour vos données, le modèle {best_model} offre une meilleure précision.",
               font=("Arial", 12)).pack(pady=5)
        
        # Graphique de comparaison
        fig, ax = plt.subplots(figsize=(8, 4))
        
        months = linear_df['mois']
        
        ax.plot(months, linear_df['revenu_predit'], 
               label='Linéaire - Revenus', marker='o', linestyle='-', alpha=0.7)
        ax.plot(months, linear_df['dépense_predite'], 
               label='Linéaire - Dépenses', marker='o', linestyle='-', alpha=0.7)
        
        ax.plot(months, forest_df['revenu_predit'], 
               label='RandomForest - Revenus', marker='x', linestyle='--', alpha=0.7)
        ax.plot(months, forest_df['dépense_predite'], 
               label='RandomForest - Dépenses', marker='x', linestyle='--', alpha=0.7)
        
        ax.set_title('Comparaison des prédictions')
        ax.set_xlabel('Mois')
        ax.set_ylabel('Montant (€)')
        plt.xticks(rotation=45)
        ax.legend()
        
        plt.tight_layout()
        
        # Affichage du graphique
        canvas = FigureCanvasTkAgg(fig, master=main_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def _export_data(self):
        """Exporte les données pour utilisation dans Power BI"""
        # Récupération des transactions
        transactions = self.db_manager.get_transactions(self.user['id'])
        
        if not transactions:
            messagebox.showinfo("Information", "Aucune donnée à exporter")
            return
        
        # Initialisation du modèle de prédiction
        prediction_model = PredictionModel(transactions)
        
        # Export des données
        success = prediction_model.export_to_csv()
        
        if success:
            messagebox.showinfo(
                "Succès", 
                f"Données exportées avec succès dans {prediction_model.export_to_csv.__defaults__[0]}"
            )
        else:
            messagebox.showerror(
                "Erreur", 
                "Échec de l'exportation des données"
            )
    
    def _on_tab_change(self, event):
        """Gère les actions lors du changement d'onglet"""
        selected_tab = self.tab_control.index(self.tab_control.select())
        
        # Mise à jour des données selon l'onglet sélectionné
        if selected_tab == 0:  # Onglet Vue générale
            self._update_overview()
        elif selected_tab == 1:  # Onglet Transactions
            self._load_transactions() 