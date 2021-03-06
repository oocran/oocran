"""
    Open Orchestrator Cloud Radio Access Network

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

"""

from math import radians, cos, sin, asin, sqrt
import numpy as np
import random
import ast
import yaml
from vnfs.models import Vnf
from scenarios.models import RRH

keys = ["name", "ip", "vnf", "bw_dl", "bw_ul", "pt", "type"]


def jsontoheat(code):
    elements = {}
    connection = {}

    operators = code['operators']
    for key,value in operators.items():
            elements[key] = value['properties']['title']

    links = code['links']
    for key,value in links.items():
        connection[value['fromOperator']] = value['toOperator']

    return elements, connection


def check_content(parameters):
    if not set(keys) <= set(parameters):
        return False


def check_parameters(parameters):
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


def read_yaml(file, operator):
    doc = yaml.load(file)

    list = []
    try:
        for rrh, parameters in doc.items():
            data = check_parameters(parameters)
            vnf = check_vnf(data['vnf'], operator)
            if check_content(parameters) is not False and data is not False and vnf is not False:
                data['name'] = data['name'] + '-' + data['ip']
                data['vnf'] = vnf
                data['operator'] = operator
                data['rrh']= RRH.objects.get(ip=data['ip'])
                data.pop('ip')
                list.append(data)
            else:
                return False
        return list
    except:
        return True


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
    return km * 1000


def price(nvf, spectre):
    price_spec = 0
    if spectre == 1400000:
        price_spec = 1.74
    if spectre == 3000000:
        price_spec = 200.0
    if spectre == 5000000:
        price_spec = 300.0
    if spectre == 10000000:
        price_spec = 400.0

    # t = int(deploy.stop.strftime("%H")) - int(deploy.start.strftime("%H"))
    price_comp = (price_spec + nvf.vnf.ram * 0.005 + nvf.vnf.cpu * 0.005)
    price = price_spec + price_comp

    return float(price)


def rb_offer(rb, total, start, stop, operation):
    value = total[1:-1].split(',')

    for i in range(stop - start + 1):
        if operation == "suma":
            value[start + i] = str(int(value[start + i]) + int(rb))
        if operation == "resta":
            value[start + i] = str(int(value[start + i]) - int(rb))

    valores = ','.join(value)
    return "[" + valores + "]"


def mcs(value, operator):
    mcs = operator.mcs
    i = 0
    for row in mcs:
        row = row.split('\n')[0]
        if row.split(',')[0] == value:
            return row.split(',')[1]
        i += 1


def optim(file):
    """
    Parser user characteristics
    """
    lista = []
    users = np.genfromtxt(file, dtype='str')

    for user in users:
        vm = {}
        vm['name'] = user.split(',')[0]
        vm['lat'] = user.split(',')[1]
        vm['long'] = user.split(',')[2]
        vm['bts'] = user.split(',')[3]
        vm['vnf'] = user.split(',')[4]
        vm['rb'] = user.split(',')[5]
        vm['mcs'] = user.split(',')[6]
        lista.append(vm)

    return lista


def rand_color():
    """
    Random color generator
    """
    r = lambda: random.randint(0, 255)
    color = ('#%02X%02X%02X' % (r(), r(), r()))
    return color


def planification_DL(nvf, colors_op, frequencies):
    start = nvf.rrh.start()
    colors = ast.literal_eval(colors_op.colors)

    if nvf.bw_dl == 1400000:
        nvf.rb = 18000000
    if nvf.bw_dl == 3000000:
        nvf.rb = 36000000
    if nvf.bw_dl == 5000000:
        nvf.rb = 72000000
    if nvf.bw_dl == 10000000:
        nvf.rb = 150000000

    assigned = [str(x) for x in nvf.rrh.freCs.split('/')]

    while True:
        if not str(start) + '-' + str(int(start) + int(nvf.bw_dl)) in frequencies:
            if not str(start) + '-' + str(int(start) + int(nvf.bw_dl)) in assigned:
                nvf.rrh.freCs = str(nvf.rrh.freCs) + '/' + str(start) + '-' + str(int(start) + int(nvf.bw_dl))
                nvf.freC_DL = int(start) + int(nvf.bw_dl) / 2
                break
            else:
                start = int(start) + int(nvf.bw_dl)
        else:
            start = int(start) + int(nvf.bw_dl)

    if colors.has_key(nvf.freC_DL):
        nvf.color_DL = colors[nvf.freC_DL]
    else:
        nvf.color_DL = rand_color()
        colors[nvf.freC_DL] = nvf.color_DL

    nvf.save()
    nvf.rrh.save()
    return nvf.rrh.freCs


def planification_UL(nvf, frequencies):
    start = int(nvf.rrh.start()) + 20000000

    nvf.color_UL = rand_color()

    assigned = [str(x) for x in nvf.rrh.freCs.split('/')]

    while (True):
        if not str(start) + '-' + str(int(start) + int(nvf.bw_ul)) in frequencies:
            if not str(start) + '-' + str(int(start) + int(nvf.bw_ul)) in assigned:
                nvf.rrh.freCs = str(nvf.rrh.freCs) + '/' + str(start) + '-' + str(int(start) + int(nvf.bw_ul))
                nvf.freC_UL = int(start) + int(nvf.bw_ul) / 2
                break
            else:
                start = int(start) + int(nvf.bw_ul)
        else:
            start = int(start) + int(nvf.bw_ul)
    nvf.save()
    nvf.rrh.save()
    return nvf.rrh.freCs
