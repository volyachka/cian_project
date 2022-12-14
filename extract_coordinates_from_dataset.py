import pandas as pd

from coordinates import *
dataset = pd.read_csv('dataset.csv', sep='\t', encoding='utf-8')
dataset['lon'] = ''
dataset['lat'] = ''
import re
dataset['oktmo_name'] = ''
COLUMN_NAME = dataset.columns.values
print(COLUMN_NAME)
preprocessed_dataframe = pd.DataFrame(columns=COLUMN_NAME)
not_process_values = list()
print(dataset.isnull().sum(axis = 0))
count = 0
for i in range(1):
    address = dataset.iloc[i]['address_line']
    address = address.replace('г Москва', 'Москва')
    address = address.replace('город Москва', 'Москва')
    moscow = address[:6]
    if moscow != 'Москва' or moscow != 'Москва':
        continue
    metros = dataset.iloc[i]['metro'].replace('[', '').replace(']', '').replace("'", "").split(', ')
    for metro in metros:
        metro = metro.replace(' (КРЛ)', '')
        address = address.replace(metro, '', 1)
    address = address.replace('ул.', 'улица')
    address = address.replace('ул,', 'улица')
    address = address.replace('ул ', 'улица ')
    address = address.replace('вл ', '')
    address = address.replace('вл', '')
    address = address.replace('пер ', 'переулок')
    address = address.replace('пер.', 'переулок')
    address = address.replace('наб ', 'набережная ')
    address = address.replace('наб.', 'набережная')
    address = address.replace('пр-кт', 'проспект')
    address = address.replace('ш.', 'шоссе')
    address = address.replace('ш ', 'шоссе')
    address = address.replace('б-р', 'бульвар')
    address = address.replace('бул', 'бульвар')
    address = address.replace('корп.', 'к')
    address = address.replace('корп ', 'к')
    address = address.replace('корп', 'к')
    address = address.replace('к.', 'к')
    address = address.replace('стр', 'с')
    address = address.replace('стр.', 'с')
    address = address.replace('с.', 'с')
    address = address.replace('м. ', '')
    for j in range(len(address)):
        if (address[j] == 'к' or address[j] == 'К') and address[j + 1].isdigit():
            address = address[:j]
            break
        if (address[j] == 'К' or address[j] == 'к') and address[j + 1] == " " and address[j + 2].isdigit():
            address = address[:j]
            break

        if (address[j] == 'с' or address[j] == 'С') and address[j + 1].isdigit():
            address = address[:j]
            break
        if (address[j] == 'с' or address[j] == 'С') and address[j + 1] == " " and address[j + 2].isdigit():
            address = address[:j]
            break
    address = address.replace(',', '')
    address = address.replace('.', '')
    address = ' '.join(address.split())
    try:
        coordinates, oktmo_name = get_coordinates_and_district_from_address_geo_tree(address)
        dataset.at[i, 'lon'] = coordinates['lon']
        dataset.at[i, 'lat'] = coordinates['lat']
        dataset.at[i, 'oktmo_name'] = oktmo_name
        preprocessed_dataframe = preprocessed_dataframe.append(dataset.iloc[i], ignore_index=True)
        print(coordinates, oktmo_name)
    except Exception as E:
        print(address)
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

print(len(not_process_values))
print(not_process_values)
preprocessed_dataframe.to_csv('preprocessed_dataframe.csv', sep='\t', encoding='utf-8')