"""
Script pour analyser le fichier de données combiné.
"""
import pandas as pd

# Charger le fichier CSV
print("Chargement du fichier...")
df = pd.read_csv('data/processed/combined_data.csv')

# Afficher des informations générales
print(f"\nInformations générales:")
print(f"- Nombre total de lignes: {len(df)}")
print(f"- Nombre total de colonnes: {len(df.columns)}")

# Liste des colonnes
print(f"\nColonnes disponibles: {', '.join(df.columns)}")

# Statistiques sur les pays et années
print(f"\nStatistiques:")
print(f"- Nombre de pays uniques: {df['country_name'].nunique()}")
print(f"- Années couvertes: {sorted(df['year'].unique())}")

# Afficher quelques lignes d'exemple
print("\nAperçu du jeu de données:")
print(df.head(3).to_string())

# Statistiques descriptives pour les indicateurs numériques principaux
numeric_cols = [
    # Indicateurs d'accès à l'éducation
    'primary_enrollment_rate',
    'secondary_enrollment_rate',
    'tertiary_enrollment_rate',
    'education_expenditure_gdp',
    'student_teacher_ratio_primary',
    'primary_completion_rate',
    'youth_literacy_rate',
    'school_life_expectancy',
    
    # Indicateurs d'égalité des genres
    'gender_ratio_primary',
    'gender_ratio_secondary',
    'gender_ratio_tertiary',
    
    # Indicateurs économiques et de pauvreté
    'gni_per_capita',
    'poverty_rate_1.9',
    'public_expenditure_per_student',
    
    # Indicateurs démographiques
    'total_population',
    'life_expectancy',
    'fertility_rate'
]

print("\nStatistiques descriptives des indicateurs principaux:")
print(df[numeric_cols].describe().round(2).to_string())

# Afficher un échantillon diversifié
print("\nÉchantillon diversifié (différents pays):")
sample = df.groupby('country_name').first().reset_index().head(5)
print(sample[['country_name', 'region', 'primary_enrollment_rate', 'gni_per_capita', 'total_population']].to_string())

# Analyse des corrélations entre les indicateurs clés
print("\nCorrélations entre les indicateurs clés:")
key_indicators = [
    'primary_enrollment_rate',
    'secondary_enrollment_rate',
    'tertiary_enrollment_rate',
    'education_expenditure_gdp',
    'gni_per_capita',
    'poverty_rate_1.9',
    'life_expectancy'
]
correlation_matrix = df[key_indicators].corr().round(2)
print(correlation_matrix.to_string()) 