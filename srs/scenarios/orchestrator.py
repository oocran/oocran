import yaml
from math import radians, cos, sin, asin, sqrt

keys = ["ip", "name", "latitude", "longitude", "pt", "neighbor", "bw","first_band","second_band","third_band"]


def check_content(parameters):
    if not set(keys) <= set(parameters):
        return False


def check_parameters(parameters):
    for k, v in parameters.items():
        if v is None:
            return False
    return {k: parameters[k] for k in set(keys) & set(parameters.keys())}


def read_yaml(file):
    doc = yaml.load(file)

    list = []
    try:
        for rrh, parameters in doc.items():
            if check_content(parameters) is not False and check_parameters(parameters) is not False:
                list.append(check_parameters(parameters))
            else:
                return False
        return list
    except:
        return None


def distance(lon1, lat1, lon2, lat2):
    """
    Calculate distance between terminal and bts
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    km = 6367 * c
    if km <=0:
        km = -km
    return km