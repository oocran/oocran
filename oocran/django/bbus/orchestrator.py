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
    """
    Check if user has this VNF
    :param data: VNF name
    :param operator:
    :return: the VNF obj
    """
    try:
        vnf = Vnf.objects.get(operator=operator, name=data)
    except:
        vnf = False
    return vnf


def read_bbus(doc, operator):
    """
    Parser the BBU parameters from yaml file
    :param doc: yaml file
    :param operator:
    :return: list of BBU parameters
    """
    keys = ["name", "ip", "vnf", "bw_dl", "bw_ul", "pt"]
    list = []
    try:
        for rrh, parameters in doc.items():
            data = check_parameters(parameters, keys)
            vnf = check_vnf(data['vnf'], operator)
            if check_content(parameters, keys) is not False:
                if data is not False:
                    if vnf is not False:
                        data['vnf'] = vnf
                        data['operator'] = operator
                        data['rrh'] = RRH.objects.get(ip=data['ip'])
                        data.pop('ip')
                        list.append(data)
                    else:
                        return "VNF is not found!", "alert alert-danger"
                else:
                    return "The content format is not valid!", "alert alert-danger"
            else:
                return "The content format is not valid!", "alert alert-danger"
        return list
    except:
        return "The content format is not valid!", "alert alert-danger"


def read_channels(doc, operator):
    """
    Parser the Channel parameters from yaml file
    :param doc: yaml file
    :param operator:
    :return: list of Channel's parameters
    """
    keys = ["vnf", "sinr", "delay", "name"]
    list = []
    try:
        for bbu, conf in doc.items():
            if conf.has_key('channel'):
                channel = conf['channel']
                data = check_parameters(channel, keys)
                vnf = check_vnf(data['vnf'], operator)
                if check_content(channel, keys) is not False:
                    if data is not False:
                        if vnf is not False:
                            data['vnf'] = vnf
                            data['bbu'] = bbu
                            list.append(data)
                        else:
                            return "VNF is not found!", "alert alert-danger"
                    else:
                        return "The content format is not valid!", "alert alert-danger"
                else:
                    return "The content format is not valid!", "alert alert-danger"
            else:
                return None
        return list
    except:
        return "The content format is not valid!", "alert alert-danger"


def read_ues(doc, operator):
    """
    Parser the UE parameters from yaml file
    :param doc: yaml file
    :param operator:
    :return: list of UE's parameters
    """
    keys = ["vnf", "cpu", "ram", "disk", "sensibility", "service", "name"]
    list = []
    try:
        for bbu, conf in doc.items():
            if conf.has_key('users'):
                users = conf['users']
                for ue, params in users.items():
                    data = check_parameters(params, keys)
                    vnf = check_vnf(data['vnf'], operator)
                    if check_content(params, keys) is not False:
                        if data is not False:
                            if vnf is not False:
                                data['vnf'] = vnf
                                data['bbu'] = bbu
                                list.append(data)
                            else:
                                return "VNF is not found!", "alert alert-danger"
                        else:
                            return "The content format is not valid!", "alert alert-danger"
                    else:
                        return "The content format is not valid!", "alert alert-danger"
            else:
                return None
        return list
    except:
        return "The content format is not valid!", "alert alert-danger"


def read_users(doc, scenario):
    """
    Parser the users parameters from yaml file
    :param doc: yaml file
    :param operator:
    :return: list of User parameters
    """
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


def price(nvf, spectre):
    """
    Calcul the VNF price
    :param nvf:
    :param spectre:
    :return: VNF price
    """
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
    """
    Search an availiable frequency band for the BBU downlink
    :param nvf:
    :param frequencies:
    :param bw:
    :return: DL assigned central frequency to VNF
    """
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
    """
    Search an availiable frequency band for the BBU uplink
    :param nvf:
    :param frequencies:
    :param bw:
    :return: UL assigned central frequency to VNF
    """
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
