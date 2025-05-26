import pandas as pd

# Définir les listes des pays par continent
pays_afrique = [
    'DZA', 'AGO', 'BEN', 'BWA', 'BFA', 'BDI', 'CMR', 'CPV', 'CAF', 'TCD', 
    'COM', 'COG', 'COD', 'DJI', 'EGY', 'GNQ', 'ERI', 'ETH', 'GAB', 'GMB', 
    'GHA', 'GIN', 'GNB', 'CIV', 'KEN', 'LSO', 'LBR', 'LBY', 'MDG', 'MWI', 
    'MLI', 'MRT', 'MUS', 'MAR', 'MOZ', 'NAM', 'NER', 'NGA', 'RWA', 'STP', 
    'SEN', 'SYC', 'SLE', 'SOM', 'ZAF', 'SSD', 'SDN', 'SWZ', 'TZA', 'TGO', 
    'TUN', 'UGA', 'ZMB', 'ZWE'
]

pays_asie = [
    'AFG', 'ARM', 'AZE', 'BHR', 'BGD', 'BTN', 'BRN', 'KHM', 'CHN', 'CYP', 
    'GEO', 'HKG', 'IND', 'IDN', 'IRN', 'IRQ', 'ISR', 'JPN', 'JOR', 'KAZ', 
    'KWT', 'KGZ', 'LAO', 'LBN', 'MAC', 'MYS', 'MDV', 'MNG', 'MMR', 'NPL', 
    'OMN', 'PAK', 'PSE', 'PHL', 'QAT', 'SAU', 'SGP', 'KOR', 'LKA', 'SYR', 
    'TWN', 'TJK', 'THA', 'TLS', 'TUR', 'TKM', 'ARE', 'UZB', 'VNM', 'YEM'
]

pays_europe = [
    'ALB', 'AND', 'AUT', 'BLR', 'BEL', 'BIH', 'BGR', 'HRV', 'CZE', 'DNK', 
    'EST', 'FIN', 'FRA', 'DEU', 'GRC', 'HUN', 'ISL', 'IRL', 'ITA', 'LVA', 
    'LIE', 'LTU', 'LUX', 'MLT', 'MDA', 'MCO', 'MNE', 'NLD', 'MKD', 'NOR', 
    'POL', 'PRT', 'ROU', 'RUS', 'SMR', 'SRB', 'SVK', 'SVN', 'ESP', 'SWE', 
    'CHE', 'UKR', 'GBR', 'VAT'
]

# Lecture des fichiers CSV
free_education = pd.read_csv('free_education.csv')
mobilite_entrant = pd.read_csv('taux_mobilité_entrant.csv')
mobilite_sortant = pd.read_csv('taux_mobilité_sortant.csv')

# Supprimer les colonnes non nécessaires
columns_to_drop = ['indicatorId', 'qualifier', 'magnitude']
free_education = free_education.drop(columns=columns_to_drop)
mobilite_entrant = mobilite_entrant.drop(columns=columns_to_drop)
mobilite_sortant = mobilite_sortant.drop(columns=columns_to_drop)

# Renommer les colonnes pour chaque dataset
column_mapping = {
    'geoUnit': 'country_code',
    'year': 'year',
    'value': 'value'
}

free_education = free_education.rename(columns=column_mapping)
mobilite_entrant = mobilite_entrant.rename(columns=column_mapping)
mobilite_sortant = mobilite_sortant.rename(columns=column_mapping)

# Filtrer les données entre 2013 et 2022
min_year = 2013
max_year = 2022

free_education = free_education[
    (free_education['year'] >= min_year) & 
    (free_education['year'] <= max_year)
]

mobilite_entrant = mobilite_entrant[
    (mobilite_entrant['year'] >= min_year) & 
    (mobilite_entrant['year'] <= max_year)
]

mobilite_sortant = mobilite_sortant[
    (mobilite_sortant['year'] >= min_year) & 
    (mobilite_sortant['year'] <= max_year)
]

# Filtrer les pays par continent
tous_pays = pays_afrique + pays_asie + pays_europe
free_education = free_education[free_education['country_code'].isin(tous_pays)]
mobilite_entrant = mobilite_entrant[mobilite_entrant['country_code'].isin(tous_pays)]
mobilite_sortant = mobilite_sortant[mobilite_sortant['country_code'].isin(tous_pays)]

# Renommer les colonnes de valeur pour chaque dataset
free_education = free_education.rename(columns={'value': 'free_education_years'})
mobilite_entrant = mobilite_entrant.rename(columns={'value': 'inbound_mobility_rate'})
mobilite_sortant = mobilite_sortant.rename(columns={'value': 'outbound_mobility_rate'})

# Fusionner les datasets
donnees_combinees = free_education.merge(
    mobilite_entrant[['country_code', 'year', 'inbound_mobility_rate']],
    on=['country_code', 'year'],
    how='outer'
).merge(
    mobilite_sortant[['country_code', 'year', 'outbound_mobility_rate']],
    on=['country_code', 'year'],
    how='outer'
)

# Ajouter la colonne région
def get_region(pays):
    if pays in pays_afrique:
        return 'Africa'
    elif pays in pays_asie:
        return 'Asia'
    elif pays in pays_europe:
        return 'Europe'
    return 'Other'

donnees_combinees['region'] = donnees_combinees['country_code'].apply(get_region)

# Trier les données
donnees_combinees = donnees_combinees.sort_values(['region', 'country_code', 'year'])

# Sauvegarder le fichier final
donnees_combinees.to_csv('unesco_data.csv', index=False)

# Afficher les statistiques
print("\nStatistiques par région :")
print("\nNombre d'enregistrements par région :")
print(donnees_combinees['region'].value_counts())

print("\nMoyennes par région :")
for region in ['Africa', 'Asia', 'Europe']:
    print(f"\n{region} :")
    region_data = donnees_combinees[donnees_combinees['region'] == region]
    print(f"Nombre moyen d'années d'éducation gratuite : {region_data['free_education_years'].mean():.2f}")
    print(f"Taux moyen de mobilité entrante : {region_data['inbound_mobility_rate'].mean():.2f}")
    print(f"Taux moyen de mobilité sortante : {region_data['outbound_mobility_rate'].mean():.2f}")

print("\nStructure des données après nettoyage :")
print(donnees_combinees.head())