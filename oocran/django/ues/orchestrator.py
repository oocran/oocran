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

from vnfs.models import Vnf


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