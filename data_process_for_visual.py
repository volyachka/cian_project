import pandas as pd
import json
import re


df = pd.read_csv('preprocessed_dataframe.csv', sep='\t', encoding='utf-8', index_col=0)

for col in df.columns:
    if 'Unnamed' in col:
        df.drop(labels=col, axis=1, inplace=True)

df = df.astype({'price_mortgage': int,
                'rooms_cnt': int,
                'lon': float,
                'lat': float,
                'dist_to_metro': float})

df['index'] = df.index


def get_metro_list(df):
    metro = set()
    for metro_list in df["metro"].unique():
        metro.update(set(json.loads(metro_list.replace('\'', '\"'))))
    metro = list(metro)
    return metro

def num_to_str(num):
    return re.sub(r"(?:\d\d\d)", lambda x: x.group(0) + " ", str(num)[::-1])[::-1]