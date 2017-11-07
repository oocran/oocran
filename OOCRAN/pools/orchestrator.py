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
from vnfs.models import Vnf
from vims.models import Vim
from scenarios.models import RRH


def check_content(parameters, keys):
    if not set(keys) <= set(parameters):
        return False


def check_parameters(parameters, keys):
    for k, v in parameters.items():
        if v is None:
            return False
    return {k: parameters[k] for k in set(keys) & set(parameters.keys())}


def check_vnf(vnf, operator):
    try:
        vnf = Vnf.objects.get(operator=operator, name=vnf)
    except:
        vnf = False
    return vnf


def check_rrh(rrh, scenario):
    try:
        rrh = RRH.objects.get(scenario=scenario, ip=rrh)
    except:
        rrh = False
    return rrh


def check_bw(bw):
    if bw == 1400000 or bw == 3000000 or bw == 5000000 or bw == 10000000 or bw == 20000000:
        return True
    else:
        return False


def check_vim(name, type):
    try:
        vim = Vim.objects.get(name=name, type=type)
    except:
        vim = False
    return vim


def read_bbus(doc, operator, scenario):
    keys = ["name", "rrh", "vnf", "bw_dl", "bw_ul", "pt", "vim"]
    list = []
    res = ""

    for bbu, parameters in doc.items():
        content = check_content(parameters, keys)
        data = check_parameters(parameters, keys)
        if content is False or data is False:
            res = "The content format is not valid!"
            break
        vnf = check_vnf(vnf=data['vnf'], operator=operator)
        if vnf is False:
            res = data['name']+": VNF is not found!"
            break
        rrh = check_rrh(rrh=data['rrh'], scenario=scenario)
        if rrh is False:
            res = data['name'] + ": RRH is not found!"
            break
        bw_dl = check_bw(bw=data['bw_dl'])
        if bw_dl is False:
            res = data['name'] + ": BW Downlink band not accessible!"
            break
        bw_ul = check_bw(bw=data['bw_ul'])
        if bw_ul is False:
            res = data['name'] + ": BW Uplink band not accessible!"
            break
        if vnf.provider == "OpenStack" or vnf.provider == "AWS" or vnf.provider == "GCE":
            vim = check_vim(name=data['vim'], type=vnf.provider)
            if vim is False:
                res = data['name']+": VIM is not registered!"
                break

        data['vnf'] = vnf
        data['operator'] = operator
        data['rrh'] = RRH.objects.get(ip=data['rrh'])
        if parameters.has_key('channel'):
            data['is_simulate'] = True
            channel = parameters['channel']
        elif parameters.has_key('users'):
            data['is_simulate'] = True
            ues = parameters['users']['ue1']
        if vnf.provider == "OpenStack" or vnf.provider == "AWS" or vnf.provider == "GCE":
            data['vim'] = vim
            list.append(data)
        else:
            del data['vim']
            list.append(data)

    if res == "":
        return list
    else:
        return res


def read_channels(doc, operator):
    keys = ["vnf", "vim","sinr", "delay", "name"]
    list = []
    res = ""

    for bbu, conf in doc.items():
        if conf.has_key('channel'):
            channel = conf['channel']
            data = check_parameters(channel, keys)
            content = check_content(channel, keys)
            if content is False or data is False:
                res = "The content format is not valid!"
                break
            vnf = check_vnf(vnf=data['vnf'], operator=operator)
            if vnf is False:
                res = data['name'] + ": VNF is not found!"
                break
            if vnf.provider == "OpenStack" or vnf.provider == "AWS" or vnf.provider == "GCE":
                vim = check_vim(name=data['vim'], type=vnf.provider)
                if vim is False:
                    res = data['name'] + ": VIM is not registered!"
                    break

            data['vnf'] = vnf
            data['bbu'] = bbu
            if vnf.provider == "OpenStack" or vnf.provider == "AWS" or vnf.provider == "GCE" and data['vim'] is not False:
                data['vim'] = vim
                list.append(data)
            else:
                del data['vim']
                list.append(data)

        if res != "":
            break

    if res != "":
        return res
    else:
        return list


def read_ues(doc, operator):
    keys = ["vnf", "vim", "sensibility", "service", "name", "latitude", "longitude"]
    list = []
    res = ""
    for bbu, conf in doc.items():
        if conf.has_key('users'):
            users = conf['users']
            for ue, params in users.items():
                content = check_content(params, keys)
                data = check_parameters(params, keys)
                if content is False or data is False:
                    res = "The content format is not valid!"
                    break
                vnf = check_vnf(vnf=data['vnf'], operator=operator)
                if vnf is False:
                    res = data['name']+": VNF is not found!"
                    break
                if vnf.provider == "OpenStack" or vnf.provider == "AWS" or vnf.provider == "GCE":
                    vim = check_vim(name=data['vim'], type=vnf.provider)
                    if vim is False:
                        res = data['name']+": VIM is not registered!"
                        break

                data['vnf'] = vnf
                data['bbu'] = bbu
                if vnf.provider == "OpenStack" or vnf.provider == "AWS" or vnf.provider == "GCE" and data['vim'] is not False:
                    data['vim'] = vim
                    list.append(data)
                else:
                    del data['vim']
                    list.append(data)

            if res != "":
                break

    if res != "":
        return res
    else:
        return list


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


def jsontoheat(code):
    elements = {}
    connection = {}

    operators = code['operators']
    for key, value in operators.items():
        elements[key] = value['properties']['title']

    links = code['links']
    for key, value in links.items():
        connection[value['fromOperator']] = value['toOperator']

    return elements, connection


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


def planification_DL(nvf, frequencies, bw):
    start = nvf.rrh.start(bw)
    colors = {}

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


def planification_UL(nvf, frequencies, bw):
    start = int(nvf.rrh.start(bw)) + 20000000

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
