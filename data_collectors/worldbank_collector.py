"""
Module pour collecter les données socio-économiques depuis l'API World Bank EdStats.
"""
import os
import time
import logging
import json
import pandas as pd
import requests
from ratelimit import limits, sleep_and_retry
from tqdm import tqdm

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import WORLDBANK_API_URL, WORLDBANK_RAW_FILE, REQUEST_TIMEOUT, MAX_RETRIES, RATE_LIMIT

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Constantes pour les régions
country_regions = {
    # African countries
    'DZ': 'Africa',  # Algeria
    'BJ': 'Africa',  # Benin
    'BW': 'Africa',  # Botswana
    'BF': 'Africa',  # Burkina Faso
    'BI': 'Africa',  # Burundi
    'CM': 'Africa',  # Cameroon
    'CV': 'Africa',  # Cape Verde
    'CF': 'Africa',  # Central African Republic
    'TD': 'Africa',  # Chad
    'KM': 'Africa',  # Comoros
    'CG': 'Africa',  # Congo
    'CD': 'Africa',  # DR Congo
    'DJ': 'Africa',  # Djibouti
    'EG': 'Africa',  # Egypt
    'GQ': 'Africa',  # Equatorial Guinea
    'ER': 'Africa',  # Eritrea
    'ET': 'Africa',  # Ethiopia
    'GA': 'Africa',  # Gabon
    'GM': 'Africa',  # Gambia
    'GH': 'Africa',  # Ghana
    'GN': 'Africa',  # Guinea
    'GW': 'Africa',  # Guinea-Bissau
    'CI': 'Africa',  # Ivory Coast
    'KE': 'Africa',  # Kenya
    'LS': 'Africa',  # Lesotho
    'LR': 'Africa',  # Liberia
    'LY': 'Africa',  # Libya
    'MG': 'Africa',  # Madagascar
    'MW': 'Africa',  # Malawi
    'ML': 'Africa',  # Mali
    'MR': 'Africa',  # Mauritania
    'MU': 'Africa',  # Mauritius
    'MA': 'Africa',  # Morocco
    'MZ': 'Africa',  # Mozambique
    'NA': 'Africa',  # Namibia
    'NE': 'Africa',  # Niger
    'NG': 'Africa',  # Nigeria
    'RW': 'Africa',  # Rwanda
    'ST': 'Africa',  # Sao Tome and Principe
    'SN': 'Africa',  # Senegal
    'SC': 'Africa',  # Seychelles
    'SL': 'Africa',  # Sierra Leone
    'SO': 'Africa',  # Somalia
    'ZA': 'Africa',  # South Africa
    'SS': 'Africa',  # South Sudan
    'SD': 'Africa',  # Sudan
    'SZ': 'Africa',  # Eswatini (Swaziland)
    'TZ': 'Africa',  # Tanzania
    'TG': 'Africa',  # Togo
    'TN': 'Africa',  # Tunisia
    'UG': 'Africa',  # Uganda
    'ZM': 'Africa',  # Zambia
    'ZW': 'Africa',  # Zimbabwe

    # Asian countries
    'AF': 'Asia',   # Afghanistan
    'AM': 'Asia',   # Armenia
    'AZ': 'Asia',   # Azerbaijan
    'BH': 'Asia',   # Bahrain
    'BD': 'Asia',   # Bangladesh
    'BT': 'Asia',   # Bhutan
    'BN': 'Asia',   # Brunei
    'KH': 'Asia',   # Cambodia
    'CN': 'Asia',   # China
    'CY': 'Asia',   # Cyprus
    'GE': 'Asia',   # Georgia
    'IN': 'Asia',   # India
    'ID': 'Asia',   # Indonesia
    'IR': 'Asia',   # Iran
    'IQ': 'Asia',   # Iraq
    'IL': 'Asia',   # Israel
    'JP': 'Asia',   # Japan
    'JO': 'Asia',   # Jordan
    'KZ': 'Asia',   # Kazakhstan
    'KW': 'Asia',   # Kuwait
    'KG': 'Asia',   # Kyrgyzstan
    'LA': 'Asia',   # Laos
    'LB': 'Asia',   # Lebanon
    'MY': 'Asia',   # Malaysia
    'MV': 'Asia',   # Maldives
    'MN': 'Asia',   # Mongolia
    'MM': 'Asia',   # Myanmar
    'NP': 'Asia',   # Nepal
    'OM': 'Asia',   # Oman
    'PK': 'Asia',   # Pakistan
    'PS': 'Asia',   # Palestine
    'PH': 'Asia',   # Philippines
    'QA': 'Asia',   # Qatar
    'SA': 'Asia',   # Saudi Arabia
    'SG': 'Asia',   # Singapore
    'KR': 'Asia',   # South Korea
    'LK': 'Asia',   # Sri Lanka
    'SY': 'Asia',   # Syria
    'TW': 'Asia',   # Taiwan
    'TJ': 'Asia',   # Tajikistan
    'TH': 'Asia',   # Thailand
    'TL': 'Asia',   # Timor-Leste
    'TR': 'Asia',   # Turkey
    'TM': 'Asia',   # Turkmenistan
    'AE': 'Asia',   # United Arab Emirates
    'UZ': 'Asia',   # Uzbekistan
    'YE': 'Asia',    # Yemen
    # European countries
    'AL': 'Albania',
    'AD': 'Andorra',
    'AT': 'Austria',
    'BY': 'Belarus',
    'BE': 'Belgium',
    'BA': 'Bosnia and Herzegovina',
    'BG': 'Bulgaria',
    'HR': 'Croatia',
    'CY': 'Cyprus',
    'CZ': 'Czech Republic',
    'DK': 'Denmark',
    'EE': 'Estonia',
    'FI': 'Finland',
    'FR': 'France',
    'DE': 'Germany',
    'GR': 'Greece',
    'HU': 'Hungary',
    'IS': 'Iceland',
    'IE': 'Ireland',
    'IT': 'Italy',
    'LV': 'Latvia',
    'LI': 'Liechtenstein',
    'LT': 'Lithuania',
    'LU': 'Luxembourg',
    'MT': 'Malta',
    'MD': 'Moldova',
    'MC': 'Monaco',
    'ME': 'Montenegro',
    'NL': 'Netherlands',
    'MK': 'North Macedonia',
    'NO': 'Norway',
    'PL': 'Poland',
    'PT': 'Portugal',
    'RO': 'Romania',
    'RU': 'Russia',
    'SM': 'San Marino',
    'RS': 'Serbia',
    'SK': 'Slovakia',
    'SI': 'Slovenia',
    'ES': 'Spain',
    'SE': 'Sweden',
    'CH': 'Switzerland',
    'UA': 'Ukraine',
    'GB': 'United Kingdom',
    'VA': 'Vatican City'
}
AFRICA = 'Africa'
ASIA = 'Asia'
EUROPE = 'Europe'

@sleep_and_retry
@limits(calls=RATE_LIMIT, period=1)
def make_request(url, params=None):
    """
    Effectue une requête HTTP avec gestion des limites de taux et des erreurs.
    
    Args:
        url (str): URL de la requête
        params (dict, optional): Paramètres de la requête
        
    Returns:
        requests.Response: Objet de réponse de la requête
    """
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            logger.warning(f"Tentative {attempt + 1}/{MAX_RETRIES} échouée: {e}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(2 ** attempt)  # Backoff exponentiel
            else:
                logger.error(f"Échec de la requête après {MAX_RETRIES} tentatives: {url}")
                raise

def get_countries_by_region(region):
    """
    Retourne la liste des codes pays pour une région donnée.
    Args:
        region (str): Nom de la région (AFRICA, EUROPE, ASIA)
    Returns:
        list: Liste des codes pays ISO-2 pour la région
    """
    return [code for code, reg in country_regions.items() if reg == region]

def get_worldbank_data(indicators=None, countries=None, years=None):
    """
    Collecte les données socio-économiques de l'API World Bank.
    
    Args:
        indicators (list, optional): Liste des indicateurs à collecter
        countries (list, optional): Liste des pays à collecter
        years (list, optional): Liste des années à collecter
        
    Returns:
        pandas.DataFrame: DataFrame contenant les données collectées
    """
    if indicators is None:
        # Indicateurs éducatifs et socio-économiques
        indicators = {
            # 🎓 Accès à l'éducation
                        # Taux de scolarisation tertiaire (%)
            "SE.XPD.TOTL.GD.ZS": "education_expenditure_gdp",     # Dépenses publiques en éducation (% du PIB)
            "SE.PRM.TCHR": "student_teacher_ratio_primary",       # Ratio élèves/enseignant (primaire)
            "SE.PRM.CMPT.ZS": "primary_completion_rate",          # Taux d'achèvement du primaire
          # Alphabétisation des jeunes (% 15-24 ans)
            "SE.SCH.LIFE": "school_life_expectancy",              # Durée moyenne de scolarisation (années)

            # ⚖️ Égalité des genres
            "SE.ENR.PRIM.FM.ZS": "gender_ratio_primary",          # Ratio filles/garçons en primaire
            "SE.ENR.SECO.FM.ZS": "gender_ratio_secondary",        # Ratio filles/garçons en secondaire
            "SE.ENR.TERT.FM.ZS": "gender_ratio_tertiary",         # Ratio filles/garçons en tertiaire

            # 💰 Économie et pauvreté
            "NY.GNP.PCAP.CD": "gni_per_capita",                   # Revenu national brut par habitant
            "SP.POV.DDAY": "poverty_rate_1.9",                     # Taux de pauvreté à 1.90$/jour
            "SE.XPD.PRIM.PC.ZS": "public_expenditure_per_student",# Dépenses gouvernementales par élève (primaire)

            # 🌍 Contexte général
            "SP.POP.TOTL": "total_population",                    # Population totale
            "SP.DYN.LE00.IN": "life_expectancy",                  # Espérance de vie à la naissance
            "SP.DYN.TFRT.IN": "fertility_rate"                    # Taux de fécondité
        }
    
    if countries is None:
        # Ne collecter que les pays d'Afrique et d'Asie
        african_countries = get_countries_by_region(AFRICA)
        asian_countries = get_countries_by_region(ASIA)
        european_countries = get_countries_by_region(EUROPE)  # Pour l'Europe, si nécessaire
        countries = african_countries + asian_countries + european_countries
        logger.info(f"Liste des pays chargée: {len(countries)} pays ({len(african_countries)} Afrique, {len(asian_countries)} Asie , {len(european_countries)} Europe) ")
    
    if years is None:
        # Par défaut, collectons les données pour les 5 dernières années
        years = list(range(2013, 2023))
    
    logger.info(f"Collecte des données World Bank pour {len(indicators)} indicateurs, {len(countries)} pays et {len(years)} années")
    
    data = []
    total_requests = len(countries) * len(years) * len(indicators)
    processed_requests = 0
    
    # Traiter tous les pays sans batching
    for country in tqdm(countries, desc="Collecte des pays"):
        for year in years:
            country_data = {
                'country_code': country,
                'country_name': country,  # Utiliser directement le code pays comme nom
                'region': country_regions.get(country, 'Unknown'),
                'year': year
            }
            # Collecter les données pour chaque indicateur
            for indicator_code, indicator_name in indicators.items():
                try:
                    url = f"{WORLDBANK_API_URL}/country/{country}/indicator/{indicator_code}"
                    params = {'date': str(year), 'format': 'json'}
                    response = make_request(url, params)
                    data_json = response.json()
                    if len(data_json) > 1 and data_json[1]:
                        value = data_json[1][0]['value']
                        country_data[indicator_name] = value
                except Exception as e:
                    logger.warning(f"Erreur lors de la collecte de {indicator_name} pour {country} en {year}: {e}")
                    country_data[indicator_name] = None
            data.append(country_data)
        # Sauvegarde intermédiaire tous les 10 pays
        if len(data) % (10 * len(years)) == 0:
            temp_df = pd.DataFrame(data)
            temp_file = f"{WORLDBANK_RAW_FILE}.temp"
            temp_df.to_csv(temp_file, index=False)
            logger.info(f"Données intermédiaires sauvegardées ({len(temp_df)} lignes)")
    # Créer le DataFrame final
    df = pd.DataFrame(data)
    logger.info(f"Collectées {len(df)} lignes de données World Bank")
    return df

def save_worldbank_data(df):
    """
    Sauvegarde les données World Bank dans un fichier CSV.
    
    Args:
        df (pandas.DataFrame): DataFrame à sauvegarder
    """
    os.makedirs(os.path.dirname(WORLDBANK_RAW_FILE), exist_ok=True)
    df.to_csv(WORLDBANK_RAW_FILE, index=False)
    logger.info(f"Données World Bank sauvegardées dans {WORLDBANK_RAW_FILE}")

def collect_worldbank_data():
    """
    Fonction principale pour collecter et sauvegarder les données World Bank.
    
    Returns:
        pandas.DataFrame: DataFrame contenant les données collectées
    """
    # Call get_worldbank_data with no countries parameter to get all countries
    df = get_worldbank_data(countries=None)
    save_worldbank_data(df)
    return df

if __name__ == "__main__":
    collect_worldbank_data()