"""
Module pour fusionner les données des différentes sources.
"""
import pandas as pd
import logging
from pathlib import Path
import sys
import os

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import UNESCO_RAW_FILE, WORLDBANK_RAW_FILE, FINAL_OUTPUT_FILE

# Dictionnaire de conversion entre codes pays 2 et 3 lettres
COUNTRY_CODE_MAPPING = {
    'AF': 'AFG', 'AO': 'AGO', 'AL': 'ALB', 'AD': 'AND', 'AE': 'ARE',
    'AM': 'ARM', 'AT': 'AUT', 'AZ': 'AZE', 'BI': 'BDI', 'BE': 'BEL',
    'BJ': 'BEN', 'BF': 'BFA', 'BD': 'BGD', 'BG': 'BGR', 'BH': 'BHR',
    'BA': 'BIH', 'BY': 'BLR', 'BN': 'BRN', 'BT': 'BTN', 'BW': 'BWA',
    'CF': 'CAF', 'CH': 'CHE', 'CN': 'CHN', 'CI': 'CIV', 'CM': 'CMR',
    'CD': 'COD', 'CG': 'COG', 'KM': 'COM', 'CV': 'CPV', 'CY': 'CYP',
    'CZ': 'CZE', 'DE': 'DEU', 'DJ': 'DJI', 'DK': 'DNK', 'DZ': 'DZA',
    'EG': 'EGY', 'ER': 'ERI', 'ES': 'ESP', 'EE': 'EST', 'ET': 'ETH',
    'FI': 'FIN', 'FR': 'FRA', 'GA': 'GAB', 'GB': 'GBR', 'GE': 'GEO',
    'GH': 'GHA', 'GN': 'GIN', 'GM': 'GMB', 'GQ': 'GNQ', 'GR': 'GRC',
    'HR': 'HRV', 'HU': 'HUN', 'ID': 'IDN', 'IN': 'IND', 'IE': 'IRL',
    'IR': 'IRN', 'IQ': 'IRQ', 'IS': 'ISL', 'IL': 'ISR', 'IT': 'ITA',
    'JO': 'JOR', 'JP': 'JPN', 'KZ': 'KAZ', 'KE': 'KEN', 'KG': 'KGZ',
    'KH': 'KHM', 'KR': 'KOR', 'KW': 'KWT', 'LA': 'LAO', 'LB': 'LBN',
    'LR': 'LBR', 'LY': 'LBY', 'LI': 'LIE', 'LK': 'LKA', 'LS': 'LSO',
    'LT': 'LTU', 'LU': 'LUX', 'LV': 'LVA', 'MA': 'MAR', 'MC': 'MCO',
    'MD': 'MDA', 'MG': 'MDG', 'MV': 'MDV', 'MK': 'MKD', 'ML': 'MLI',
    'MT': 'MLT', 'MM': 'MMR', 'ME': 'MNE', 'MN': 'MNG', 'MZ': 'MOZ',
    'MR': 'MRT', 'MU': 'MUS', 'MW': 'MWI', 'MY': 'MYS', 'NA': 'NAM',
    'NE': 'NER', 'NG': 'NGA', 'NL': 'NLD', 'NO': 'NOR', 'NP': 'NPL',
    'OM': 'OMN', 'PK': 'PAK', 'PH': 'PHL', 'PL': 'POL', 'PT': 'PRT',
    'PS': 'PSE', 'QA': 'QAT', 'RO': 'ROU', 'RU': 'RUS', 'RW': 'RWA',
    'SA': 'SAU', 'SD': 'SDN', 'SN': 'SEN', 'SG': 'SGP', 'SL': 'SLE',
    'SM': 'SMR', 'RS': 'SRB', 'SS': 'SSD', 'ST': 'STP', 'SK': 'SVK',
    'SI': 'SVN', 'SE': 'SWE', 'SZ': 'SWZ', 'SC': 'SYC', 'SY': 'SYR',
    'TD': 'TCD', 'TG': 'TGO', 'TH': 'THA', 'TJ': 'TJK', 'TM': 'TKM',
    'TL': 'TLS', 'TN': 'TUN', 'TR': 'TUR', 'TZ': 'TZA', 'UG': 'UGA',
    'UA': 'UKR', 'UZ': 'UZB', 'VN': 'VNM', 'YE': 'YEM', 'ZA': 'ZAF',
    'ZM': 'ZMB', 'ZW': 'ZWE'
}

def normalize_country_codes(df, column='country_code', to_alpha3=False):
    """
    Normalise les codes pays pour assurer la cohérence.
    Args:
        df: DataFrame à normaliser
        column: Nom de la colonne contenant les codes pays
        to_alpha3: Si True, convertit en code 3 lettres, sinon en code 2 lettres
    """
    if column in df.columns:
        # Supprimer les espaces et mettre en majuscules
        df[column] = df[column].astype(str).str.strip().str.upper()
        # Remplacer les valeurs invalides par None
        df[column] = df[column].replace(['', 'NAN', 'NONE', 'NA'], None)
        
        if to_alpha3:
            # Convertir de 2 lettres vers 3 lettres
            df[column] = df[column].map(lambda x: COUNTRY_CODE_MAPPING.get(x, x))
        else:
            # Convertir de 3 lettres vers 2 lettres
            reverse_mapping = {v: k for k, v in COUNTRY_CODE_MAPPING.items()}
            df[column] = df[column].map(lambda x: reverse_mapping.get(x, x))
    
    return df

def print_country_stats(df, source):
    """
    Affiche les statistiques sur les codes pays.
    """
    valid_codes = df[df['country_code'].notna()]['country_code'].unique()
    logger.info(f"{source} - Nombre de codes pays valides: {len(valid_codes)}")
    logger.info(f"{source} - Exemples de codes pays: {sorted(valid_codes)[:10]}")

def load_worldbank_data():
    """
    Charge les données World Bank avec les colonnes spécifiques.
    """
    logger.info("Chargement des données World Bank")
    wb_columns = [
        'country_code', 'country_name', 'region', 'year',
        'education_expenditure_gdp', 'student_teacher_ratio_primary',
        'primary_completion_rate', 'school_life_expectancy',
        'gender_ratio_primary', 'gender_ratio_secondary',
        'gender_ratio_tertiary', 'gni_per_capita',
        'public_expenditure_per_student', 'total_population',
        'life_expectancy', 'fertility_rate'
    ]
    
    wb_df = pd.read_csv(WORLDBANK_RAW_FILE)
    wb_df = normalize_country_codes(wb_df)
    
    # Supprimer les lignes sans code pays
    wb_df = wb_df.dropna(subset=['country_code'])
    
    # S'assurer que toutes les colonnes requises existent
    missing_cols = [col for col in wb_columns if col not in wb_df.columns]
    if missing_cols:
        logger.warning(f"Colonnes manquantes dans World Bank data: {missing_cols}")
    
    # Sélectionner uniquement les colonnes disponibles
    available_cols = [col for col in wb_columns if col in wb_df.columns]
    wb_df = wb_df[available_cols]
    
    print_country_stats(wb_df, "World Bank")
    return wb_df

def load_unesco_data():
    """
    Charge les données UNESCO avec les colonnes spécifiques.
    """
    logger.info("Chargement des données UNESCO")
    unesco_columns = [
        'country_code', 'year',
        'free_education_years',
        'inbound_mobility_rate',
        'outbound_mobility_rate'
    ]
    
    try:
        unesco_df = pd.read_csv(UNESCO_RAW_FILE)
        
        # Convertir les codes pays UNESCO (3 lettres) en codes 2 lettres si nécessaire
        unesco_df = normalize_country_codes(unesco_df, to_alpha3=False)
        
        # Supprimer les lignes sans code pays
        unesco_df = unesco_df.dropna(subset=['country_code'])
        
        # Sélectionner uniquement les colonnes requises
        available_cols = [col for col in unesco_columns if col in unesco_df.columns]
        unesco_df = unesco_df[available_cols]
        
        print_country_stats(unesco_df, "UNESCO")
        return unesco_df
        
    except Exception as e:
        logger.error(f"Erreur lors du chargement des données UNESCO: {str(e)}")
        raise

def merge_datasets():
    """
    Fusionne les datasets World Bank et UNESCO.
    """
    # Charger les données
    wb_df = load_worldbank_data()
    unesco_df = load_unesco_data()
    
    # Obtenir la liste des pays dans World Bank
    worldbank_countries = set(wb_df['country_code'].unique())
    unesco_countries = set(unesco_df['country_code'].unique())
    
    # Afficher les statistiques de correspondance des pays
    common_countries = worldbank_countries.intersection(unesco_countries)
    logger.info(f"Nombre de pays en commun: {len(common_countries)}")
    logger.info(f"Pays présents uniquement dans World Bank: {sorted(worldbank_countries - unesco_countries)}")
    logger.info(f"Pays présents uniquement dans UNESCO: {sorted(unesco_countries - worldbank_countries)}")
    
    # Filtrer les données UNESCO pour ne garder que les pays de World Bank
    unesco_df = unesco_df[unesco_df['country_code'].isin(worldbank_countries)]
    logger.info(f"Données UNESCO filtrées: {len(unesco_df)} lignes")
    
    # Fusion sur country_code et year
    merged_df = pd.merge(
        wb_df,
        unesco_df,
        on=['country_code', 'year'],
        how='left'
    )
    
    # Supprimer la colonne country_name
    if 'country_name' in merged_df.columns:
        merged_df = merged_df.drop('country_name', axis=1)
        logger.info("Colonne country_name supprimée")
    
    # Trier les données
    merged_df = merged_df.sort_values(['country_code', 'year'])
    
    logger.info(f"Dataset final: {len(merged_df)} lignes")
    return merged_df

def save_merged_data(df):
    """
    Sauvegarde le dataset fusionné.
    """
    output_dir = os.path.dirname(FINAL_OUTPUT_FILE)
    os.makedirs(output_dir, exist_ok=True)
    
    df.to_csv(FINAL_OUTPUT_FILE, index=False)
    logger.info(f"Données fusionnées sauvegardées dans {FINAL_OUTPUT_FILE}")
    
    # Afficher les informations sur les colonnes
    logger.info("Colonnes dans le dataset final:")
    for col in df.columns:
        non_null = df[col].count()
        total = len(df)
        percentage = (non_null / total) * 100
        logger.info(f"{col}: {non_null}/{total} valeurs non-null ({percentage:.2f}%)")

def merge_all_data():
    """
    Fonction principale pour fusionner toutes les données.
    """
    merged_df = merge_datasets()
    save_merged_data(merged_df)
    return merged_df

if __name__ == "__main__":
    merge_all_data()
