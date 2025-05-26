# Projet DAjuc - Analyse des Données Éducatives

Ce projet est une solution complète pour l'analyse des données éducatives, comprenant la collecte, le traitement, la visualisation et la présentation des données sur l'éducation à travers le monde.

## Objectifs du Projet

- Collecter et homogénéiser des données éducatives depuis diverses sources (UNESCO, World Bank, GeoNames)
- Analyser l'impact des politiques de gratuité sur la durée des études
- Évaluer la rétention scolaire dans différentes régions
- Créer des visualisations interactives pour l'exploration des données

## Structure du Projet

```
.
├── data_collectors/          # Scripts de collecte de données
│   ├── unesco_collector.py   # Données UNESCO UIS
│   ├── worldbank_collector.py # Données World Bank
├── data_processing/          # Traitement des données
│   ├── data_cleaner.py      # Nettoyage des données
│   └── data_merger.py       # Fusion des données
├── data/                    # Stockage des données
├── EDA.ipynb               # Notebook d'analyse exploratoire
├── dashboard.py            # Interface interactive Streamlit
├── main.py                 # Point d'entrée principal
├── config.py              # Configuration du projet
└── requirements.txt       # Dépendances Python
```

## Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

## Installation

1. Clonez le dépôt :
```bash
git clone [URL_DU_REPO]
cd Projet-DAjuc
```

2. Créez un environnement virtuel et activez-le :
```bash
python -m venv venv
# Sur Windows
venv\Scripts\activate
# Sur Unix/MacOS
source venv/bin/activate
```

3. Installez les dépendances :
```bash
pip install -r requirements.txt
```

## Utilisation

### 1. Collecte et Traitement des Données

Pour exécuter le pipeline complet de collecte et de traitement des données :
```bash
python main.py
```

### 2. Exploration des Données

Pour l'analyse exploratoire des données, ouvrez le notebook Jupyter :
```bash
jupyter notebook EDA.ipynb
```

### 3. Dashboard Interactif

Pour lancer le dashboard interactif :
```bash
streamlit run dashboard.py
```


## Fonctionnalités Principales

- **Collecte de Données** : Extraction automatisée depuis UNESCO, World Bank et GeoNames
- **Traitement** : Nettoyage, normalisation et fusion des données
- **Visualisation** : Dashboard interactif avec Streamlit
- **Analyse** : Notebook Jupyter pour l'exploration approfondie


