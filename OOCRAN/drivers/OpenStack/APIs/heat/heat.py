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

from heatclient.client import Client
from time import sleep
from drivers.OpenStack.APIs.keystone.keystone import get_project_id
from drivers.OpenStack.APIs.keystone.keystone import get_token


def credentials(domain, username, project_domain_name, project_name, password, ip, operator_name, operator_password):
    heat = Client('1',
                  endpoint="http://" + ip + ":8004/v1/" + get_project_id(domain=domain, username=username, project_domain_name=project_domain_name, project_name=project_name, password=password, ip=ip, operator_name=operator_name),
                  token=get_token(domain=domain, username=operator_name, project_domain_name=project_domain_name, project_name=operator_name, password=operator_password, ip=ip))
    return heat


def create_stack(name, template, domain, username, project_domain_name, project_name, password, ip, operator_name, operator_password):
    heat = credentials(domain, username, project_domain_name, project_name, password, ip, operator_name, operator_password)
    stack = heat.stacks.create(stack_name=name, template=template, parameters={})
    uid = stack['stack']['id']

    stack = heat.stacks.get(stack_id=uid).to_dict()
    while stack['stack_status'] == 'CREATE_IN_PROGRESS':
        print "Creating stack."
        stack = heat.stacks.get(stack_id=uid).to_dict()
        sleep(10)

    if stack['stack_status'] == 'CREATE_COMPLETE':
        print "Stack succesfully created."
        return stack['outputs']
    else:
        return "Stack fall to unknow status: {}".format(stack)


def delete_stack(name, domain, username, project_domain_name, project_name, password, ip, operator_name, operator_password):
    heat = credentials(domain, username, project_domain_name, project_name, password, ip, operator_name, operator_password)
    stack = heat.stacks.get(name)
    heat.stacks.delete(stack.parameters['OS::stack_id'])