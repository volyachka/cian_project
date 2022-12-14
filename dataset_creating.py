import pandas as pd
dataset = pd.read_csv('dataset.csv', sep='\t', encoding='utf-8')
dataset['lon'] = ''
dataset['lat'] = ''
dataset['oktmo_name'] = ''
COLUMN_NAME = dataset.columns.values
preprocessed_dataframe = pd.DataFrame(columns=COLUMN_NAME)
preprocessed_dataframe.to_csv('preprocessed_dataframe.csv', sep='\t', encoding='utf-8')
dataset.to_csv('dataset.csv', sep='\t', encoding='utf-8')