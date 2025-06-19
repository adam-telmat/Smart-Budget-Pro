# Smart Budget Pro

## Description

Smart Budget Pro est un outil financier conçu pour les PME, permettant de gérer les revenus, les dépenses et d'obtenir des prédictions basées sur l'intelligence artificielle. Ce projet combine une interface utilisateur intuitive avec une base de données sécurisée et des capacités d'analyse prédictive.

![Smart Budget Pro](https://img.shields.io/badge/Smart%20Budget%20Pro-v1.0-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-brightgreen)
![SQLite](https://img.shields.io/badge/SQLite-3.0-orange)
![License](https://img.shields.io/badge/License-MIT-green)

## Fonctionnalités

- **Interface utilisateur** : Interface graphique Tkinter intuitive avec authentification sécurisée
- **Gestion des transactions** : Ajout, recherche et visualisation des transactions financières
- **Sécurité intégrée** : Hachage des mots de passe et validation des entrées pour prévenir les injections SQL
- **Prédictions IA** : Analyse des tendances financières avec régression linéaire et RandomForest
- **Visualisations** : Graphiques interactifs des revenus et dépenses actuels et prévus
- **Export de données** : Génération de fichiers CSV compatibles avec Power BI

## Installation

### Prérequis

- Python 3.8 ou supérieur

### Installation des dépendances

```bash
pip install pandas numpy matplotlib scikit-learn
```

### Cloner le dépôt

```bash
git clone https://github.com/votre-username/Smart-Budget-Pro.git
cd Smart-Budget-Pro
```

## Utilisation

### Lancement de l'application

```bash
python -m app.main
```

### Première utilisation

1. Créez un compte utilisateur via l'écran d'inscription
2. Connectez-vous à votre compte
3. Commencez à enregistrer vos transactions financières
4. Explorez les fonctionnalités d'analyse et de prédiction

## Configuration Power BI

1. Lancez l'application et exportez les données via le bouton "Exporter données" dans l'onglet Vue générale
2. Ouvrez Power BI Desktop
3. Cliquez sur "Obtenir les données" > "Fichier texte"
4. Sélectionnez le fichier `budget_predictions.csv` généré
5. Créez un graphique linéaire avec les colonnes de dates en axe X et les montants en axe Y
6. Ajoutez un tableau avec les recommandations et prédictions

## Structure du projet

- `app/main.py`: Point d'entrée de l'application
- `app/config/`: Configurations et constantes
- `app/database/`: Gestionnaire de base de données et scripts SQL
- `app/models/`: Modèles prédictifs et logique métier
- `app/views/`: Interfaces utilisateur Tkinter
- `app/utils/`: Fonctions utilitaires

## Sécurité

- **Mots de passe**: Hachés avec SHA-256 avant stockage
- **Validation des entrées**: Vérification stricte pour empêcher les injections
- **Protection des données**: Conception avec isolation des couches d'accès

## Développement

### Tests

Vérifiez le bon fonctionnement de l'application:

```bash
# Vérifier l'export CSV
python -c "from app.models.prediction_model import PredictionModel; print(PredictionModel([]).export_to_csv())"

# Vérifier l'initialisation de la base de données
python -c "from app.database.db_manager import DatabaseManager; print(DatabaseManager().initialize_database())"
```

## License

Ce projet est distribué sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.
