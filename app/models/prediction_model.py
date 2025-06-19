#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Smart Budget Pro - Modèle de prédiction IA

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
import csv
import os

from app.config.settings import PREDICTION_MONTHS, DATE_FORMAT, EXPORT_PATH, ALERT_THRESHOLD

class PredictionModel:
    """Classe gérant les prédictions financières basées sur l'IA"""
    
    def __init__(self, transactions_data):
        """
        Initialise le modèle de prédiction avec les données de transactions
        
        Args:
            transactions_data: Liste de tuples (id, reference, description, montant, date, type)
        """
        self.raw_data = transactions_data
        self.df = self._prepare_data()
        
    def _prepare_data(self):
        """
        Prépare les données pour l'analyse et les prédictions
        
        Returns:
            DataFrame avec les données agrégées par mois
        """
        # Création d'un DataFrame à partir des données brutes
        df = pd.DataFrame(self.raw_data, 
                         columns=['id', 'reference', 'description', 'montant', 'date', 'type'])
        
        # Conversion des dates
        df['date'] = pd.to_datetime(df['date'], format=DATE_FORMAT)
        
        # Création de la colonne mois-année
        df['mois'] = df['date'].dt.strftime('%Y-%m')
        
        # Calcul des revenus et dépenses mensuels
        monthly_income = df[df['type'] == 'revenu'].groupby('mois')['montant'].sum()
        monthly_expense = df[df['type'] == 'dépense'].groupby('mois')['montant'].sum()
        
        # Création d'un DataFrame pour l'analyse
        result_df = pd.DataFrame({
            'revenu': monthly_income,
            'dépense': monthly_expense
        }).fillna(0)
        
        # Ajout d'une colonne pour le solde mensuel
        result_df['solde'] = result_df['revenu'] - result_df['dépense']
        
        # Création des indices numériques pour la prédiction
        result_df.reset_index(inplace=True)
        result_df['month_index'] = range(len(result_df))
        
        return result_df
    
    def predict_linear_regression(self):
        """
        Effectue des prédictions financières en utilisant la régression linéaire
        
        Returns:
            DataFrame avec les prédictions pour les prochains mois
        """
        if len(self.df) < 2:
            # Pas assez de données pour faire une prédiction
            return pd.DataFrame(), 0, "Données insuffisantes"
        
        # Création des features (X) et des targets (y) pour les revenus et dépenses
        X = self.df[['month_index']].values
        y_income = self.df['revenu'].values
        y_expense = self.df['dépense'].values
        
        # Création et entraînement des modèles de régression
        income_model = LinearRegression()
        expense_model = LinearRegression()
        
        income_model.fit(X, y_income)
        expense_model.fit(X, y_expense)
        
        # Génération des mois futurs pour prédiction
        last_month_index = self.df['month_index'].max()
        future_indices = np.array(range(last_month_index + 1, last_month_index + 1 + PREDICTION_MONTHS)).reshape(-1, 1)
        
        # Prédictions
        future_income = income_model.predict(future_indices)
        future_expense = expense_model.predict(future_indices)
        
        # Création des dates futures
        if len(self.df) > 0:
            last_date = datetime.strptime(self.df['mois'].iloc[-1], '%Y-%m')
        else:
            last_date = datetime.now().replace(day=1)
            
        future_dates = [(last_date + timedelta(days=30*i)).strftime('%Y-%m') 
                        for i in range(1, PREDICTION_MONTHS + 1)]
        
        # Création du DataFrame de prédictions
        predictions_df = pd.DataFrame({
            'mois': future_dates,
            'revenu_predit': future_income,
            'dépense_predite': future_expense,
            'solde_predit': future_income - future_expense
        })
        
        # Calcul du R² pour les modèles
        y_income_pred = income_model.predict(X)
        y_expense_pred = expense_model.predict(X)
        
        income_r2 = r2_score(y_income, y_income_pred) if len(y_income) > 1 else 0
        expense_r2 = r2_score(y_expense, y_expense_pred) if len(y_expense) > 1 else 0
        
        # Score moyen R²
        avg_r2 = (income_r2 + expense_r2) / 2
        
        # Générer une recommandation
        total_future_income = sum(future_income)
        total_future_expense = sum(future_expense)
        
        recommendation = "Finances stables" 
        if total_future_income == 0:
            recommendation = "Données insuffisantes"
        elif total_future_expense > (total_future_income * ALERT_THRESHOLD):
            recommendation = "Alerte: Réduire les dépenses"
            
        return predictions_df, avg_r2, recommendation
    
    def predict_random_forest(self):
        """
        Effectue des prédictions financières en utilisant Random Forest
        
        Returns:
            DataFrame avec les prédictions pour les prochains mois
        """
        if len(self.df) < 2:
            # Pas assez de données pour faire une prédiction
            return pd.DataFrame(), 0, "Données insuffisantes"
        
        # Création des features (X) et des targets (y) pour les revenus et dépenses
        X = self.df[['month_index']].values
        y_income = self.df['revenu'].values
        y_expense = self.df['dépense'].values
        
        # Création et entraînement des modèles Random Forest
        income_model = RandomForestRegressor(n_estimators=100, random_state=42)
        expense_model = RandomForestRegressor(n_estimators=100, random_state=42)
        
        income_model.fit(X, y_income)
        expense_model.fit(X, y_expense)
        
        # Génération des mois futurs pour prédiction
        last_month_index = self.df['month_index'].max()
        future_indices = np.array(range(last_month_index + 1, last_month_index + 1 + PREDICTION_MONTHS)).reshape(-1, 1)
        
        # Prédictions
        future_income = income_model.predict(future_indices)
        future_expense = expense_model.predict(future_indices)
        
        # Création des dates futures
        if len(self.df) > 0:
            last_date = datetime.strptime(self.df['mois'].iloc[-1], '%Y-%m')
        else:
            last_date = datetime.now().replace(day=1)
            
        future_dates = [(last_date + timedelta(days=30*i)).strftime('%Y-%m') 
                        for i in range(1, PREDICTION_MONTHS + 1)]
        
        # Création du DataFrame de prédictions
        predictions_df = pd.DataFrame({
            'mois': future_dates,
            'revenu_predit': future_income,
            'dépense_predite': future_expense,
            'solde_predit': future_income - future_expense
        })
        
        # Calcul du R² pour les modèles
        y_income_pred = income_model.predict(X)
        y_expense_pred = expense_model.predict(X)
        
        income_r2 = r2_score(y_income, y_income_pred) if len(y_income) > 1 else 0
        expense_r2 = r2_score(y_expense, y_expense_pred) if len(y_expense) > 1 else 0
        
        # Score moyen R²
        avg_r2 = (income_r2 + expense_r2) / 2
        
        # Générer une recommandation
        total_future_income = sum(future_income)
        total_future_expense = sum(future_expense)
        
        recommendation = "Finances stables" 
        if total_future_income == 0:
            recommendation = "Données insuffisantes"
        elif total_future_expense > (total_future_income * ALERT_THRESHOLD):
            recommendation = "Alerte: Réduire les dépenses"
            
        return predictions_df, avg_r2, recommendation
    
    def export_to_csv(self):
        """
        Exporte les données réelles et prédites vers un fichier CSV
        
        Returns:
            bool: True si l'export a réussi, False sinon
        """
        try:
            # Obtenir les prédictions
            predictions_df, r2_score, recommendation = self.predict_linear_regression()
            
            if len(predictions_df) == 0:
                return False
                
            # Préparer les données à exporter
            historical_data = self.df[['mois', 'revenu', 'dépense', 'solde']].copy()
            historical_data['est_prediction'] = False
            historical_data['recommandation'] = ""
            
            # Préparer les prédictions
            predictions = predictions_df.copy()
            predictions.columns = ['mois', 'revenu', 'dépense', 'solde']
            predictions['est_prediction'] = True
            predictions['recommandation'] = recommendation
            
            # Combiner les données historiques et les prédictions
            export_data = pd.concat([historical_data, predictions], ignore_index=True)
            
            # Exporter vers CSV
            export_data.to_csv(EXPORT_PATH, index=False)
            
            return True
        except Exception as e:
            print(f"Erreur lors de l'export CSV: {e}")
            return False 