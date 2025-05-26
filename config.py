"""
Configuration du pipeline de collecte et traitement de données.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Chemins de base
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# S'assurer que les répertoires existent
os.makedirs(RAW_DATA_DIR, exist_ok=True)
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)

# Configuration des sources de données
UNESCO_BASE_URL = "http://api.uis.unesco.org/sdmx"
WORLDBANK_API_URL = "https://api.worldbank.org/v2"

# Clés API - à remplacer par vos clés réelles
# Idéalement, ces clés devraient être stockées dans un fichier .env

UNESCO_API_KEY = os.getenv("UNESCO_API_KEY")
WORLDBANK_APP_ID = os.getenv("WORLDBANK_APP_ID", "demo")
WORLDBANK_APP_KEY = os.getenv("WORLDBANK_APP_KEY", "demo")

# Paramètres des requêtes
REQUEST_TIMEOUT = 30  # secondes
MAX_RETRIES = 3
RATE_LIMIT = 5  # Nombre maximal de requêtes par seconde

# Chemins des fichiers de sortie
UNESCO_RAW_FILE = RAW_DATA_DIR / "unesco_data.csv"
WORLDBANK_RAW_FILE = RAW_DATA_DIR / "worldbank_data2.csv"  # Updated to match actual filename

FINAL_OUTPUT_FILE = PROCESSED_DATA_DIR / "combined_data.csv"

# Mappings des noms de pays pour l'homogénéisation


# Colonnes à conserver dans le fichier final
FINAL_COLUMNS = [
    'country_code',
    'year',
    'region',
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
    'gni_per_capita',
    'public_expenditure_per_student',
    'total_population',
    'life_expectancy',
    'fertility_rate'
]