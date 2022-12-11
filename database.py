import pandas as pd
import json

path = "/home/volya/project/pythonProject14/cian_project/spider_cian/items.json"
with open(path) as f:
    dataset = pd.read_json(f)
