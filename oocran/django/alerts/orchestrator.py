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

import yaml
from math import radians, cos, sin, asin, sqrt

keys = ["ip", "name", "latitude", "longitude", "pt", "neighbor", "bw","first_band","second_band","third_band"]


def check_content(parameters):
    """
    Check if yaml file has all the necessary parameters
    :param parameters:  necessary parameters to create the NS
    :return: False if the user forgot any parameter
    """
    if not set(keys) <= set(parameters):
        return False


def check_parameters(parameters):
    """
    Check if any yaml file parameter is null
    :param parameters: necessary parameters to create the NS
    :return:
    """
    for k, v in parameters.items():
        if v is None:
            return False
    return {k: parameters[k] for k in set(keys) & set(parameters.keys())}


def read_yaml(file):
    """
    Read the yaml file parameters
    :param file:
    :return:
    """
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