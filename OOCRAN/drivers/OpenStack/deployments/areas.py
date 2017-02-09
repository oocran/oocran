from jinja2 import Template
from drivers.OpenStack.APIs.heat.heat import create_stack, delete_stack


def create_area(scenario):
    file = Template(u'''\
heat_template_version: 2013-05-23

description: {{description}}

parameters:

resources:
  mgmt_net:
    type: OS::Neutron::Net
    properties:
      name: {{name}}_mgmt_net

  mgmt_subnet:
    type: OS::Neutron::Subnet
    properties:
      name: {{name}}_mgmt_subnet
      network_id: { get_resource: mgmt_net }
      cidr: 10.0.0.0/24
      gateway_ip: 10.0.0.1
      allocation_pools:
        - start: 10.0.0.2
          end: 10.0.0.254

  bbu_net:
    type: OS::Neutron::Net
    properties:
      name: {{name}}_bbu_net

  bbu_subnet:
    type: OS::Neutron::Subnet
    properties:
      name: {{name}}_bbu_subnet
      network_id: { get_resource: bbu_net }
      cidr: 20.0.0.0/24
      gateway_ip: 20.0.0.1
      allocation_pools:
        - start: 20.0.0.2
          end: 20.0.0.254

  router:
    type: OS::Neutron::Router
    properties:
      name: {{name}}_router
      external_gateway_info:
        network: 0e67e979-6fb8-485a-923f-1c5d57351e76

  interface_bbu:
    type: OS::Neutron::RouterInterface
    properties:
      router_id: { get_resource: router }
      subnet_id: { get_resource: bbu_subnet }

  interface_mgmt:
    type: OS::Neutron::RouterInterface
    properties:
      router_id: { get_resource: router }
      subnet_id: { get_resource: mgmt_subnet }
  ''')
    template = file.render(
        description=scenario.description,
        name=scenario.name
    )

    create_stack(scenario, template, scenario.vim)


def delete_area(scenario):
    delete_stack(scenario, scenario.vim)