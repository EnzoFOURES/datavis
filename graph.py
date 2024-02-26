import pandas as pd
import matplotlib.pyplot as plt

# Chargement des données
file_path_dec = 'dataset_aqi.csv'
file_path_jan = 'aqi_predictions_advanced.csv'

# Lecture des données
data_dec = pd.read_csv(file_path_dec, delimiter=';')
data_jan = pd.read_csv(file_path_jan)

# Conversion de la colonne 'DATE' en datetime
data_dec['DATE'] = pd.to_datetime(data_dec['DATE'])
data_jan['DATE'] = pd.to_datetime(data_jan['DATE'])

# Filtrage des données pour décembre 2023
data_dec = data_dec[(data_dec['DATE'] >= '2023-12-01') & (data_dec['DATE'] <= '2023-12-31')]

# Grouper par date et calculer la moyenne de l'AQI pour décembre 2023
data_dec_mean = data_dec.groupby(data_dec['DATE'].dt.date)['AQI'].mean().reset_index()

# Filtrage des données pour janvier 2024
data_jan = data_jan[(data_jan['DATE'] >= '2024-01-01') & (data_jan['DATE'] <= '2024-01-31')]

# Création des graphiques
plt.figure(figsize=(18, 6))

# Graphique pour décembre 2023
plt.subplot(1, 3, 1)
plt.plot(data_dec_mean['DATE'], data_dec_mean['AQI'], label='Décembre 2023', color='blue')
plt.title('AQI pour Décembre 2023')
plt.xlabel('Date')
plt.ylabel('AQI (µg/m³)')
plt.xticks(rotation=45)
plt.grid(True)

# Graphique pour janvier 2024
plt.subplot(1, 3, 2)
plt.plot(data_jan['DATE'], data_jan['AQI'], label='Janvier 2024', color='green')
plt.title('AQI pour Janvier 2024')
plt.xlabel('Date')
plt.ylabel('AQI (µg/m³)')
plt.xticks(rotation=45)
plt.grid(True)

# Graphique combiné
plt.subplot(1, 3, 3)
plt.plot(data_dec_mean['DATE'], data_dec_mean['AQI'], label='Décembre 2023', color='blue')
plt.plot(data_jan['DATE'], data_jan['AQI'], label='Janvier 2024', color='green')
plt.title('Comparaison des AQI')
plt.xlabel('Date')
plt.ylabel('AQI (µg/m³)')
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)

# Ajustement de la mise en page et affichage du graphique
plt.tight_layout()
plt.show()
