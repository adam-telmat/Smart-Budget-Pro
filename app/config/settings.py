#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Smart Budget Pro - Fichier de configuration

# Configuration de l'application
APP_TITLE = "Smart Budget Pro"
APP_SIZE = "800x600"
VERSION = "1.0.0"

# Configuration de la base de données
DB_PATH = "app/database/smart_budget.db"

# Configuration des prédictions
PREDICTION_MONTHS = 6
ALERT_THRESHOLD = 1.10  # Alerte si dépenses > 110% des revenus

# Configuration des exports
EXPORT_PATH = "budget_predictions.csv"

# Autres paramètres
DATE_FORMAT = "%Y-%m-%d"
PASSWORD_MIN_LENGTH = 8 