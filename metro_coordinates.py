# function_for_find_metro_coordinates
from dadata import Dadata
from information import *
def extract_metro_coordinates(metro_names):
    token = "dd7e408388d191b2d000e775cfdf5e1c4283f63f"
    dadata = Dadata(token)
    metro_coordinates = dict()
    for key in metro_names:
        try:
            request = dadata.suggest("metro", key)[0]['data']
            metro_coordinates[key] = dict()
            metro_coordinates[key]['lon'] = request['geo_lon']
            metro_coordinates[key]['lat'] = request['geo_lat']
        except Exception as E:
            pass
    return metro_coordinates