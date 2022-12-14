import pandas as pd
from functions_to_work_with_coordinates import *
from information import *
def extract_regions():
    preprocessed_dataframe = pd.read_csv('preprocessed_dataframe.csv', sep='\t', encoding='utf-8')
    print(len(preprocessed_dataframe))
    for i in range(len(preprocessed_dataframe)):
        district = preprocessed_dataframe.iloc[i]['district']
        for region, districts in regions.items():
            print(region)
            if district in districts:
                preprocessed_dataframe.at[i, 'region'] = region
    preprocessed_dataframe.to_csv('preprocessed_dataframe.csv', sep='\t', encoding='utf-8')
