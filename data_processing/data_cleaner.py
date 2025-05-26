"""
Module pour nettoyer et normaliser les données.
"""
import pandas as pd
import logging
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))
from config import UNESCO_RAW_FILE, WORLDBANK_RAW_FILE

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def normalize_country_names(df):
    """
    Normalise les noms et codes de pays.
    """
    # Vérifier si la colonne country_code existe
    if 'country_code' not in df.columns:
        logger.warning("Colonne country_code manquante")
        return df
        
    # Convertir les codes pays en majuscules
    df['country_code'] = df['country_code'].str.upper()
    
    # Supprimer la colonne country_name si elle existe
    if 'country_name' in df.columns:
        df = df.drop('country_name', axis=1)
        logger.info("Colonne country_name supprimée")
    
    return df

def normalize_numeric_values(df):
    """
    Normalise les valeurs numériques.
    """
    # Liste des colonnes à traiter comme numériques
    numeric_columns = [
        'free_education_years',
        'inbound_mobility_rate',
        'outbound_mobility_rate',
        'education_expenditure_gdp',
        'student_teacher_ratio_primary',
        'primary_completion_rate',
        'school_life_expectancy',
        'gender_ratio_primary',
        'gender_ratio_secondary',
        'gender_ratio_tertiary',
        'public_expenditure_per_student'
    ]
    
    for col in numeric_columns:
        if col in df.columns:
            # Convertir en numérique, les erreurs deviennent NaN
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # Remplacer les valeurs aberrantes par NaN
            # Par exemple, les taux ne devraient pas dépasser 100%
            if 'rate' in col or 'ratio' in col:
                df[col] = df[col].clip(0, 100)
                
    return df

def clean_unesco_data(df):
    """
    Nettoie et normalise les données UNESCO.
    """
    if df.empty:
        return df
    
    logger.info("Nettoyage des données UNESCO")
    
    # Normaliser les noms de pays
    df = normalize_country_names(df)
    
    # Normaliser les valeurs numériques
    df = normalize_numeric_values(df)
    
    # Supprimer les doublons
    df = df.drop_duplicates()
    
    return df

def clean_worldbank_data(df):
    """
    Nettoie et normalise les données World Bank.
    """
    if df.empty:
        return df
    
    logger.info("Nettoyage des données World Bank")
    
    # Normaliser les noms de pays
    df = normalize_country_names(df)
    
    # Normaliser les valeurs numériques
    df = normalize_numeric_values(df)
    
    # Supprimer les doublons
    df = df.drop_duplicates()
    
    return df

def clean_all_data():
    """
    Nettoie toutes les données sources.
    
    Returns:
        tuple: (unesco_df, worldbank_df) DataFrames nettoyés
    """
    # Charger et nettoyer les données UNESCO
    try:
        unesco_df = pd.read_csv(UNESCO_RAW_FILE)
        unesco_df = clean_unesco_data(unesco_df)
    except Exception as e:
        logger.error(f"Erreur lors du nettoyage des données UNESCO: {e}")
        unesco_df = pd.DataFrame()

    # Charger et nettoyer les données World Bank
    try:
        worldbank_df = pd.read_csv(WORLDBANK_RAW_FILE)
        worldbank_df = clean_worldbank_data(worldbank_df)
    except Exception as e:
        logger.error(f"Erreur lors du nettoyage des données World Bank: {e}")
        worldbank_df = pd.DataFrame()

    return unesco_df, worldbank_df