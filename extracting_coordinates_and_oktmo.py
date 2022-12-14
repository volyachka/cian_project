import pandas as pd

from functions_to_work_with_coordinates import *
import re
from preprocess import *

def coordinates_extracting():
    dataset = pd.read_csv('dataset.csv', sep='\t', encoding='utf-8')
    preprocessed_dataframe = pd.read_csv('preprocessed_dataframe.csv', sep='\t', encoding='utf-8')
    COLUMN_NAME = dataset.columns.values
    print(COLUMN_NAME)
    not_process_values = list()
    save_i = list()
    for i in range(len(dataset)):
        address = dataset.iloc[i]['address_line']
        address = address.replace('г Москва', 'Москва')
        address = address.replace('город Москва', 'Москва')
        moscow = address[:6]
        if moscow != 'Москва':
            continue  # мы работаем только с квартирами в москве
        metros = dataset.iloc[i]['metro'].replace('[', '').replace(']', '').replace("'", "").split(', ')
        for metro in metros:  # удаляем из адреса все вхождения станций метро
            metro = preprocess_metro(metro)
            address = address.replace(metro, '', 1)

        # парсим адрес
        address = address_preprocessing(address)
        try:
            coordinates, oktmo_name = get_coordinates_and_district_from_address_geo_tree(address)
            dataset.at[i, 'lon'] = coordinates['lon']
            dataset.at[i, 'lat'] = coordinates['lat']
            dataset.at[i, 'oktmo_name'] = oktmo_name
            preprocessed_dataframe = preprocessed_dataframe.append(dataset.iloc[i], ignore_index=True)
        except Exception as E:
            not_process_values.append(i)
            try:
                address = dataset.iloc[i]['street']
                m = re.findall(r'\d+', dataset.iloc[i]['address_line'])
                if m:
                    address += m[0]
                coordinates, oktmo_name = get_coordinates_and_district_from_address_geo_tree(address)
                dataset.at[i, 'lon'] = coordinates['lon']
                dataset.at[i, 'lat'] = coordinates['lat']
                dataset.at[i, 'oktmo_name'] = oktmo_name
                preprocessed_dataframe = preprocessed_dataframe.append(dataset.iloc[i], ignore_index=True)
            except Exception as E:
                not_process_values.append(i)

        # тестовое сохранение, чтобы проверить, что все работает
        if i == 10:
            preprocessed_dataframe.to_csv('preprocessed_dataframe.csv', sep='\t', encoding='utf-8')
        # будем сохранять наш датасет каждые 500 эпох, если программа упадет, некоторые данные уцелеют
        if i % 500 == 0:
            preprocessed_dataframe.to_csv('preprocessed_dataframe.csv', sep='\t', encoding='utf-8')
            save_i.append(i)
    print(save_i)  # чтобы узнать, на каком упало
    preprocessed_dataframe.to_csv('preprocessed_dataframe.csv', sep='\t', encoding='utf-8')
