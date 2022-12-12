import requests
import json
def get_coordinates_and_district_from_address_geo_tree(address):
    response = requests.get(f'https://api.geotree.ru/address.php?key=5dhomJ1lXlmz&term={address}&oktmo=45000000')
    data = response.text
    data = json.loads(data)
    print(data[0]['geo_center'], data[0]['oktmo_name'])
    return data[0]['geo_center'], data[0]['oktmo_name']


def get_coordinates_from_address_2_gis(address):
#чтобы запрос работал, нужно обязательно указывать город Москва, иначе тильт
    response = requests.get(f'https://catalog.api.2gis.com/3.0/items/geocode?q={address}&fields=items.point&key=ruaofg3859')
    data = response.text
    data = json.loads(data)
    print(data['result']['items'][0]['point'])
    return data['result']['items'][0]['point']


def get_distance_between_two_coordinates(sources_point, list_of_targets):
    #Запрос вернет длину маршрута в метрах (distance) и время в пути в секундах (duration) для каждой пары точек отправления-прибытия.
    #
    data = {
        "type": "statistics",
        "sources": [0],
        'targets': [],
        'points': []
    }
    for i in range(len(list_of_targets)):
        data['targets'].append(i + 1)
    data['points'].append(sources_point)
    data['points'].extend(list_of_targets)
    print(data)
    data = json.dumps(data)
    response = requests.post('https://routing.api.2gis.com/get_dist_matrix?key=9ea2d981-c362-441e-b53e-d5dc26add861&version=2.0', data)
    data = response.text
    data = json.loads(data)
    return data['routes'][0]['distance'], data['routes'][0]['duration']

# sources_point = {"lat": 54.99770587584445, "lon": 82.79502868652345}
# list_of_targets = [{"lat": 54.99928130973027, "lon": 82.92137145996095}]
# get_distance_between_two_coordinates(sources_point, list_of_targets)