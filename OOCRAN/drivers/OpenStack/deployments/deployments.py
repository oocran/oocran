from jinja2 import Template
from drivers.OpenStack.APIs.heat.heat import create_stack, delete_stack


def add_nfs(user, nfs):
    elements = ""
    num = 0

    for nf in nfs:
        nf_template = Template(u'''\
nf_{{num}}:
    type: OS::Heat::SoftwareConfig
    properties:
      group: ungrouped
      config: |
        #!/bin/sh
        cd /home/{{user}}
        {{script}}

  ''')

        nf_template = nf_template.render(
            num=num,
            user=user,
            script=nf.script,
        )
        elements = elements + nf_template
        num += 1

    return [num, elements]


def add_nvf(user, nvfs):
    elements = ""
    num = 0

    for nvf in nvfs:
        [nfs_num, nfs] = add_nfs(user, nvf.vnf.nf.all())

        t = Template(u'''\
server{{num}}_init:
    type: OS::Heat::MultipartMime
    properties:
      parts:
      - config: {get_resource: user_config}
      - config: {get_resource: credentials}
{{nfs}}

  server{{num}}_port:
    type: OS::Neutron::Port
    properties:
      network_id: network
      fixed_ips:
        - subnet_id: network

  server{{num}}_floating_ip:
    type: OS::Neutron::FloatingIP
    properties:
      floating_network: provider
      port_id: { get_resource: server{{num}}_port }


  server{{num}}:
    type: OS::Nova::Server
    properties:
      name: {{name}}
      image: {{image}}
      flavor: {{flavor}}
      networks:
        - port: { get_resource: server{{num}}_port }
      user_data_format: RAW
      user_data:
         get_resource: server{{num}}_init

  ''')
        list_nfs = ""
        for nf in range(0, nfs_num):
            list_nfs += "      - config: {get_resource: nf_" + str(nf) + "}"

        t = t.render(
            name=nvf.name,
            image=nvf.vnf.name,
            flavor="small",
            num=num,
            nfs=list_nfs,
        )
        elements += nfs + t
        num += 1

    return elements


def create_deploy(ns, bbus, channels=None, ues=None):

    header = Template(u'''\
heat_template_version: 2014-10-16
description: {{description}}

parameters:
  NetID:
    type: string
    description: Network ID to use for the instance.
    default: net

resources:
  credentials:
    type: OS::Heat::CloudConfig
    properties:
      cloud_config:
        chpasswd:
          list: |
            {{user}}:{{password}}
          expire: False

  user_config:
    type: OS::Heat::CloudConfig
    properties:
      cloud_config:
        users:
        - default
        - name: {{user}}

  ''')
    header = header.render(
        description=ns.description,
        user=ns.operator.user.username,
        password=ns.operator.password,
    )

    list_bbus = add_nvf(ns.operator.user.username, bbus)
    if channels is not None:
        list_channels = add_nvf(ns.operator.user.username, channels)
    if ues is not None:
        list_ues = add_nvf(ns.operator.user.username, ues)

    template = header + list_bbus + list_channels + list_ues
    print template
    create_stack(ns, template, ns.scenario.vim)


def delete_deploy(ns):
    delete_stack(ns, ns.scenario.vim)
