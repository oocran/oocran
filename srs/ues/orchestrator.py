from math import radians, cos, sin, asin, sqrt
import numpy as np
import random
from vnfs.models import Vnf
from scenarios.models import RRH


def check_content(parameters, keys):
    if not set(keys) <= set(parameters):
        return False


def check_parameters(parameters, keys):
    for k, v in parameters.items():
        if v is None:
            return False
    return {k: parameters[k] for k in set(keys) & set(parameters.keys())}


def check_vnf(data, operator):
    try:
        vnf = Vnf.objects.get(operator=operator, name=data)
    except:
        vnf = False
    return vnf


def read_users(doc, scenario):
    keys = ["latitude", "longitude", "sensibility", "service", "name"]
    list = []
    try:
        for ue, parameters in doc.items():
            data = check_parameters(parameters, keys)
            if check_content(parameters, keys) is not False:
                if data is not False:
                    data['scenario'] = scenario
                    data['operator'] = scenario.operator
                    list.append(data)
                else:
                    return "The content format is not valid!", "alert alert-danger"
            else:
                return "The content format is not valid!", "alert alert-danger"
        return list,  "alert alert-success"
    except:
        return "The content format is not valid!", "alert alert-danger"