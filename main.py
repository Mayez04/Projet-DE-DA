"""
Script principal pour exécuter le pipeline de traitement des données.
"""
import logging
from data_processing.data_cleaner import clean_unesco_data, clean_worldbank_data
from data_processing.data_merger import merge_all_data
import pandas as pd
from config import UNESCO_RAW_FILE, WORLDBANK_RAW_FILE

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """
    Exécute le pipeline complet de traitement des données.
    """
    try:
        # Charger et nettoyer les données UNESCO
        logger.info("Chargement des données UNESCO")
        unesco_df = pd.read_csv(UNESCO_RAW_FILE)
        unesco_df = clean_unesco_data(unesco_df)
        
        # Charger et nettoyer les données World Bank
        logger.info("Chargement des données World Bank")
        wb_df = pd.read_csv(WORLDBANK_RAW_FILE)
        wb_df = clean_worldbank_data(wb_df)
        
        # Fusionner les données
        logger.info("Fusion des données")
        merged_df = merge_all_data()
        
        logger.info("Pipeline de traitement terminé avec succès")
        
    except Exception as e:
        logger.error(f"Erreur lors du traitement: {str(e)}")
        raise

if __name__ == "__main__":
    main()