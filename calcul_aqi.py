import pandas as pd
import numpy as np
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Fonction pour nettoyer et convertir les valeurs numériques, y compris les valeurs spéciales comme '<2'
def clean_numeric_special(value):
    try:
        value = str(value).replace(',', '.')
        if '<' in value:
            return float(value[1:])
        return float(value)
    except ValueError:
        return np.nan


# Fonction pour calculer le sous-indice pour chaque polluant en utilisant les nouveaux seuils
def calculate_sub_index_new(pollutant, concentration, reference_values):
    thresholds = reference_values.get(pollutant, [])
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
    sub_indices = [calculate_sub_index_new(pollutant, row[pollutant], reference_values)
                   for pollutant in reference_values.keys()]
    aqi = max(sub_indices)

    # Déterminer le statut en fonction de l'AQI
    if aqi <= 50:
        statut = 'Bon'
    elif aqi <= 150:
        statut = 'Modéré'
    elif aqi <= 300:
        statut = 'Dangereux'
    else:
        statut = 'Très dangereux'

    # Logging du statut
    logging.info(f"AQI: {aqi}, Statut: {statut}")

    return aqi, statut


# Fonction principale mise à jour
def main_new():
    # Chemin du fichier CSV
    file_path = r'C:\Users\enzof\PycharmProjects\datavis\qualite-air-mesuree-auber.csv'

    # Lecture du fichier CSV
    data = pd.read_csv(file_path, delimiter=';')

    # Renommer la colonne 'DATE/HEURE' en 'DATE'
    data.rename(columns={'DATE/HEURE': 'DATE'}, inplace=True)

    # Nettoyage et formatage de la colonne 'DATE'
    data['DATE'] = pd.to_datetime(data['DATE'], errors='coerce', utc=True)
    data['DATE'] = data['DATE'].dt.strftime('%Y-%m-%d')

    # Nettoyage et conversion des colonnes de données
    for col in ['NO', 'NO2', 'PM10', 'PM2.5', 'CO2', 'TEMP', 'HUMI']:
        data[col] = data[col].apply(clean_numeric_special)

    # Suppression des lignes avec des valeurs manquantes pour les polluants
    data.dropna(subset=['NO', 'NO2', 'PM10', 'PM2.5', 'CO2', 'TEMP', 'HUMI'], inplace=True)

    # Valeurs de référence et facteurs de conversion
    reference_values = {
        'NO': [40, 120, 200],  # µg/m³
        'NO2': [40, 180, 240],  # µg/m³
        'PM10': [50, 80, 120],  # µg/m³
        'PM2.5': [25, 50, 75],  # µg/m³
        'CO2': [1000, 1500, 2000],  # ppm
        'TEMP': [35, 40, 45],  # °C
        'HUMI': [95, 100, 105]  # %
    }

    # Calcul de l'AQI avec les nouveaux seuils et ajout de la colonne STATUT
    data[['AQI', 'STATUT']] = data.apply(lambda row: calculate_aqi_new(row, reference_values), axis=1,
                                         result_type='expand')

    # Sauvegarde du fichier avec les colonnes AQI et STATUT ajoutées
    output_file = r'C:\Users\enzof\PycharmProjects\datavis\dataset_aqi.csv'
    data.to_csv(output_file, index=False, sep=';')

    print("Calcul de l'AQI terminé et fichier sauvegardé.")


if __name__ == "__main__":
    main_new()