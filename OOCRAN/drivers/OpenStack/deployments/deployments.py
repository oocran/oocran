from jinja2 import Template
from drivers.OpenStack.APIs.heat.heat import create_stack, delete_stack


def add_nfs(nvf):
    elements = ""
    num_nf = 0

    for nf in nvf.vnf.nf.all():
        if nf.check_libraries() is not False:
            for library in nf.get_libraries_order():
                nf_template = Template(u'''\
{{name}}_nf{{nf}}:
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
                    name=nvf.name,
                    nf=num_nf,
                    user=nvf.operator.name,
                    library=library.script.replace('\n', '\n        '),
                )
                elements += nf_template
                num_nf += 1

    return [num_nf, elements]


def add_launch(user, nvf):
    elements = ""
    num = 0

    for nf in nvf.vnf.nf.all():
        nf_template = Template(u'''\
{{name}}_launch:
    type: OS::Heat::SoftwareConfig
    properties:
      group: ungrouped
      config: |
        #!/bin/sh
        cd /home/{{user}}
{{script}}

  ''')
        cmds = nf.script.split("\n")
        for cmd in cmds:
            script = "        " + cmd + "\n        "

        nf_template = nf_template.render(
            name=nvf.name,
            user=user,
            script=script,
        )
        elements += nf_template
        num += 1

    return elements


def add_nvf(user, nvfs):
    elements = ""

    for nvf in nvfs:
        [nfs_num, nfs] = add_nfs(nvf)
        launch = add_launch(user, nvf)

        t = Template(u'''\
{{name}}_init:
    type: OS::Heat::MultipartMime
    properties:
      parts:
      - config: {get_resource: user_config}
      - config: {get_resource: credentials}
{{nfs}}

  {{name}}_port:
    type: OS::Neutron::Port
    properties:
      name: {{name}}
      network_id: network
      fixed_ips:
        - subnet_id: network

  {{name}}_floating_ip:
    type: OS::Neutron::FloatingIP
    properties:
      floating_network: provider
      port_id: { get_resource: {{name}}_port }

  {{name}}:
    type: OS::Nova::Server
    properties:
      name: {{name}}
      image: {{image}}
      flavor: {{flavor}}
      networks:
        - port: { get_resource: {{name}}_port }
      user_data_format: RAW
      user_data:
         get_resource: {{name}}_init

  ''')
        list_nfs = ""
        for nf in range(0, nfs_num):
            list_nfs += "      - config: {get_resource: " + nvf.name + "_nf" + str(nf) + "}\n"

        list_nfs += "      - config: {get_resource: " + nvf.name + "_launch}"

        t = t.render(
            name=nvf.name,
            image=nvf.vnf.image,
            flavor="small",
            nfs=list_nfs,
        )
        elements += nfs + launch + t

    return elements


def outputs(nvfs):
    outputs = ""
    for nvf in nvfs:
        output = Template(u'''\
{{name}}:
    value: { get_attr: [ {{name}}_floating_ip, floating_ip_address ] }
  ''')

        output = output.render(
            name=nvf.name,
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
        users:
          - name: {{user}}
            sudo: ['ALL=(ALL) NOPASSWD:ALL']
            groups: sudo
            shell: /bin/bash
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

    output = Template(u'''\

outputs:
  ''')
    output = output.render()

    output += outputs(bbus)
    output += outputs(channels)
    output += outputs(ues)

    template = header + list_bbus + list_channels + list_ues + output
    print template
    ips = create_stack(name=ns.name,
                       template=template,
                       domain=ns.vim.domain,
                       username=ns.vim.username,
                       project_domain_name=ns.vim.project_domain,
                       project_name=ns.vim.project,
                       password=ns.vim.password,
                       ip=ns.vim.ip,
                       operator_name=ns.operator.name,
                       operator_password=ns.operator.password)

    for ip in ips:
        for nvf in bbus:
            if nvf.name == ip['output_key']:
                nvf.mgmt_ip = ip['output_value']
                nvf.save()
        if channels is not None:
            for nvf in channels:
                if nvf.name == ip['output_key']:
                    nvf.mgmt_ip = ip['output_value']
                    nvf.save()
        if ues is not None:
            for nvf in ues:
                if nvf.name == ip['output_key']:
                    nvf.mgmt_ip = ip['output_value']
                    nvf.save()


def delete_deploy(ns):
    delete_stack(name=ns.name,
                 domain=ns.vim.domain,
                 username=ns.vim.username,
                 project_domain_name=ns.vim.project_domain,
                 project_name=ns.vim.project,
                 password=ns.vim.password,
                 ip=ns.vim.ip,
                 operator_name=ns.operator.name,
                 operator_password=ns.operator.password)
