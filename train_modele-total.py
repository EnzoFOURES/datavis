import pandas as pd  # Importation de la bibliothèque pandas pour le traitement de données
import numpy as np  # Importation de la bibliothèque numpy pour le traitement de données
import logging  # Importation du module logging pour la journalisation

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Fonction pour nettoyer et convertir les valeurs numériques, y compris les valeurs spéciales comme '<2'
def clean_numeric_special(value):
    try:
        value = str(value).replace(',', '.')  # Remplace les virgules par des points
        if '<' in value:  # Vérifie si '<' est présent dans la valeur
            return float(value[1:])  # Convertit la valeur à partir de l'index 1 en flottant
        return float(value)  # Convertit la valeur en flottant
    except ValueError:  # Capture les erreurs de conversion en flottant
        return np.nan  # Retourne np.nan en cas d'erreur

# Fonction pour calculer le sous-indice pour chaque polluant en utilisant les nouveaux seuils
def calculate_sub_index_new(pollutant, concentration, reference_values):
    thresholds = reference_values.get(pollutant, [])  # Récupère les seuils pour le polluant donné
    if concentration <= thresholds[0]:
        return 50  # Bon
    elif concentration <= thresholds[1]:
        return 150  # Modéré
    elif concentration <= thresholds[2]:
        return 300  # Dangereux
    else:
        return 500  # Très dangereux, mort imminente

# Fonction pour calculer l'AQI avec les nouveaux seuils
def calculate_aqi_new(row, reference_values):
    # Calcule les sous-indices pour chaque polluant et les stocke dans une liste
    sub_indices = [calculate_sub_index_new(pollutant, row[pollutant], reference_values) for pollutant in reference_values.keys()]
    aqi = max(sub_indices)  # Détermine l'indice de qualité de l'air (AQI) comme le maximum des sous-indices

    # Détermine le statut en fonction de l'AQI
    if aqi <= 50:
        statut = 'Bon'
    elif aqi <= 150:
        statut = 'Modéré'
    elif aqi <= 300:
        statut = 'Dangereux'
    else:
        statut = 'Très dangereux'

    # Enregistre le statut dans les logs
    logging.info(f"AQI: {aqi}, Statut: {statut}")

    return aqi, statut

# Fonction principale mise à jour
def main_new():
    # Chemin du fichier CSV contenant les données de qualité de l'air
    file_path = r'C:\Users\enzof\PycharmProjects\datavis\qualite-air-mesuree-auber.csv'

    # Lecture du fichier CSV dans un DataFrame pandas
    data = pd.read_csv(file_path, delimiter=';')

    # Renomme la colonne 'DATE/HEURE' en 'DATE'
    data.rename(columns={'DATE/HEURE': 'DATE'}, inplace=True)

    # Nettoie et formate la colonne 'DATE'
    data['DATE'] = pd.to_datetime(data['DATE'], errors='coerce', utc=True)
    data['DATE'] = data['DATE'].dt.strftime('%Y-%m-%d')

    # Nettoie et convertit les colonnes de données numériques
    for col in ['NO', 'NO2', 'PM10', 'PM2.5', 'CO2', 'TEMP', 'HUMI']:
        data[col] = data[col].apply(clean_numeric_special)

    # Supprime les lignes avec des valeurs manquantes pour les polluants
    data.dropna(subset=['NO', 'NO2', 'PM10', 'PM2.5', 'CO2', 'TEMP', 'HUMI'], inplace=True)

    # Définit les valeurs de référence et facteurs de conversion pour les polluants
    reference_values = {
        'NO': [40, 120, 200],   # µg/m³
        'NO2': [40, 180, 240],  # µg/m³
        'PM10': [50, 80, 120],  # µg/m³
        'PM2.5': [25, 50, 75],  # µg/m³
        'CO2': [1000, 1500, 2000],  # ppm
        'TEMP': [35, 40, 45],   # °C
        'HUMI': [95, 100, 105]  # %
    }

    # Calcule l'AQI avec les nouveaux seuils et ajoute la colonne STATUT
    data[['AQI', 'STATUT']] = data.apply(lambda row: calculate_aqi_new(row, reference_values), axis=1, result_type='expand')

    # Sauvegarde du fichier avec les colonnes AQI et STATUT ajoutées
    output_file = r'C:\Users\enzof\PycharmProjects\datavis\dataset_aqi.csv'
    data.to_csv(output_file, index=False, sep=';')

    print("Calcul de l'AQI terminé et fichier sauvegardé.")


if __name__ == "__main__":
    main_new()
