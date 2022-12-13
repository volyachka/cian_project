import pandas as pd
import json

path_1 = "/home/volya/project/pythonProject14/cian_project/spider_cian/spider_cian/items_form_1_to_299.json"
with open(path_1) as f:
    dataset_1 = pd.read_json(f)

path_1 = "/home/volya/project/pythonProject14/cian_project/spider_cian/spider_cian/items_from_300_to_599.json"
with open(path_1) as f:
    dataset_2 = pd.read_json(f)

path_1 = "/home/volya/project/pythonProject14/cian_project/spider_cian/spider_cian/items_from_600_to_899.json"
with open(path_1) as f:
    dataset_3 = pd.read_json(f)

path_1 = "/home/volya/project/pythonProject14/cian_project/spider_cian/spider_cian/items_from_900_to_1308.json"
with open(path_1) as f:
    dataset_4 = pd.read_json(f)

# df_merged = dataset_1.append(dataset_2, ignore_index=True).append(dataset_3, ignore_index=True)

dataset = pd.concat([dataset_1, dataset_2, dataset_3, dataset_4], ignore_index=True)
