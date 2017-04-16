from jinja2 import Template
from drivers.OpenStack.APIs.heat.heat import create_stack, delete_stack


def create_infrastructure(operator, vim):
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

    create_stack(name="infrastructure",
                 template=template,
                 domain=vim.domain,
                 username=vim.username,
                 project_domain_name=vim.project_domain,
                 project_name=vim.project,
                 password=vim.password,
                 ip=vim.ip,
                 operator_name=operator.name,
                 operator_password=operator.password)


def delete_area(scenario):
    delete_stack(scenario, scenario.vim)