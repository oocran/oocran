from jinja2 import Template
from drivers.OpenStack.APIs.heat.heat import create_stack, delete_stack


def add_nfs(vnf, num_vnf):
    elements = ""
    num_nf = 0

    for nf in vnf.nf.all():
        for library in nf.get_libraries_order():
            nf_template = Template(u'''\
vnf{{num}}_nf{{nf}}:
    type: OS::Heat::SoftwareConfig
    properties:
      group: {{group}}
      config: |
        #!/bin/sh
        cd /home/{{user}}
        {{library}}

  ''')

            nf_template = nf_template.render(
                group=library.type,
                num=num_vnf,
                nf=num_nf,
                user=vnf.operator.name,
                library=library.script,
            )
            elements += nf_template
            num_nf += 1

    return [num_nf, elements]


def add_launch(user, vnf, num_vnf):
    elements = ""
    num = 0

    for nf in vnf.nf.all():
        nf_template = Template(u'''\
vnf{{num}}_launch:
    type: OS::Heat::SoftwareConfig
    properties:
      group: ungrouped
      config: |
        #!/bin/sh
        cd /home/{{user}}
        {{script}}

  ''')

        nf_template = nf_template.render(
            num=num_vnf,
            user=user,
            script=nf.script,
        )
        elements += nf_template
        num += 1

    return elements


def add_nvf(user, nvfs, num_vnf):
    elements = ""

    for nvf in nvfs:
        [nfs_num, nfs] = add_nfs(nvf.vnf, num_vnf)
        launch = add_launch(user, nvf.vnf, num_vnf)

        t = Template(u'''\
vnf{{num}}_init:
    type: OS::Heat::MultipartMime
    properties:
      parts:
      - config: {get_resource: user_config}
      - config: {get_resource: credentials}
{{nfs}}

  vnf{{num}}_port:
    type: OS::Neutron::Port
    properties:
      name: {{name}}
      network_id: network
      fixed_ips:
        - subnet_id: network

  vnf{{num}}_floating_ip:
    type: OS::Neutron::FloatingIP
    properties:
      floating_network: provider
      port_id: { get_resource: vnf{{num}}_port }

  vnf{{num}}:
    type: OS::Nova::Server
    properties:
      name: {{name}}
      image: {{image}}
      flavor: {{flavor}}
      networks:
        - port: { get_resource: vnf{{num}}_port }
      user_data_format: RAW
      user_data:
         get_resource: vnf{{num}}_init

  ''')
        list_nfs = ""
        for nf in range(0, nfs_num):
            list_nfs += "      - config: {get_resource: vnf" + str(num_vnf) + "_nf" + str(nf) + "}\n"

        list_nfs += "      - config: {get_resource: vnf" + str(num_vnf) + "_launch}"

        t = t.render(
            name=nvf.name,
            image=nvf.vnf.image,
            flavor="small",
            num=num_vnf,
            nfs=list_nfs,
        )
        elements += nfs + launch + t
        num_vnf += 1

    return elements, num_vnf


def outputs(num):
    outputs = Template(u'''\

outputs:
  ''')
    outputs = outputs.render()

    for nvf in range(0, num):
        output = Template(u'''\
vnf{{num}}_mgmt:
    value: { get_attr: [ vnf{{num}}, networks, provider, 0 ] }
  ''')

        output = output.render(
            num=nvf,
        )
        outputs += output
    return outputs


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

    num = 0
    [list_bbus, num] = add_nvf(ns.operator.user.username, bbus, num)
    if channels is not None:
        [list_channels, num] = add_nvf(ns.operator.user.username, channels, num)
    if ues is not None:
        [list_ues, num] = add_nvf(ns.operator.user.username, ues, num)

    output = outputs(num)

    template = header + list_bbus + list_channels + list_ues + output
    print template
    '''create_stack(name=ns.name,
                 template=template,
                 domain=ns.vim.domain,
                 username=ns.vim.username,
                 project_domain_name=ns.vim.project_domain,
                 project_name=ns.vim.project,
                 password=ns.vim.password,
                 ip=ns.vim.ip,
                 operator_name=ns.operator.name,
                 operator_password=ns.operator.password)'''


def delete_deploy(ns):
    '''delete_stack(name=ns.name,
                 domain=ns.vim.domain,
                 username=ns.vim.username,
                 project_domain_name=ns.vim.project_domain,
                 project_name=ns.vim.project,
                 password=ns.vim.password,
                 ip=ns.vim.ip,
                 operator_name=ns.operator.name,
                 operator_password=ns.operator.password)'''
