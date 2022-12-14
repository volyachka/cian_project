from metro_coordinates import *
import pandas as pd
from functions_to_work_with_coordinates import *
from metro_coordinates import *
from preprocess import *


def distance_to_metro_extracting():
    preprocessed_dataframe = pd.read_csv('preprocessed_dataframe.csv', sep='\t', encoding='utf-8')
    for i in range(len(preprocessed_dataframe)):
        metros = preprocessed_dataframe.iloc[i]['metro'].replace('[', '').replace(']', '').replace("'", "").split(', ')
        min_distance_to_metro = 1e6
        if len(metros) == 0:
            continue
        for metro in metros:  # удаляем из адреса все вхождения станций метро
            try:
                metro = preprocess_metro(metro)
                metro = metro.lower()
                current_distance = distanceInKmBetweenEarthCoordinates(metro_coordinates[metro]['lat'],
                                                                       metro_coordinates[metro]['lon'],
                                                                       preprocessed_dataframe.iloc[i]['lat'],
                                                                       preprocessed_dataframe.iloc[i]['lon'])
                min_distance_to_metro = min(min_distance_to_metro, current_distance)
            except Exception as E:
                pass
        preprocessed_dataframe.at[i, 'dist_to_metro'] = min_distance_to_metro

    preprocessed_dataframe.to_csv('preprocessed_dataframe.csv', sep='\t', encoding='utf-8')

# distance_to_metro_extracting()
# preprocessed_dataframe = pd.read_csv('preprocessed_dataframe.csv', sep='\t', encoding='utf-8')
# print(preprocessed_dataframe.iloc[10000])
