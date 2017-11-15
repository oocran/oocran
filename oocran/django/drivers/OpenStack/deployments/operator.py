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

from jinja2 import Template
from drivers.OpenStack.APIs.heat.heat import create_stack, delete_stack


def create_operator(operator, vim):
    file = Template(u'''\
heat_template_version: 2013-05-23

description: infrastructure

parameters:

resources:
  network:
    type: OS::Neutron::Net
    properties:
      name: network

  subnet:
    type: OS::Neutron::Subnet
    properties:
      name: network
      network_id: { get_resource: network }
      cidr: 10.0.0.0/24
      gateway_ip: 10.0.0.1
      dns_nameservers: [ "8.8.8.8", "8.8.4.4" ]
      allocation_pools:
        - start: 10.0.0.2
          end: 10.0.0.254

  router:
    type: OS::Neutron::Router
    properties:
      name: router
      external_gateway_info:
        network: {{external}}

  interface_bbu:
    type: OS::Neutron::RouterInterface
    properties:
      router_id: { get_resource: router }
      subnet_id: { get_resource: subnet }

  ''')
    template = file.render(
        external=vim.public_network,
    )

    print template

    create_stack(name="infrastructure",
                 template=template,
                 domain=vim.domain,
                 username=vim.username,
                 project_domain_name=vim.project_domain,
                 project_name=vim.project,
                 password=vim.decrypt(),
                 ip=vim.ip,
                 operator_name=operator.name,
                 operator_password=operator.decrypt())


def delete_area(scenario):
    delete_stack(scenario, scenario.vim)