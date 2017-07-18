from jinja2 import Template
from drivers.OpenStack.APIs.heat.heat import create_stack, delete_stack
from drivers.OpenStack.APIs.nova.nova import get_flavors


def scripts(nvf):
    elements = ""
    count = 0

    for script in nvf.vnf.get_scripts_order():
        element = Template(u'''\
{{name}}_nf{{nf}}:
    type: OS::Heat::SoftwareConfig
    properties:
      group: {{group}}
      config: |
        #!/bin/sh
        cd /home/{{user}}
        {{code}}

  ''')
        group = script.type
        if group == "file" or group == "script":
            group = "ungrouped"
        element = element.render(
            group=group,
            name=nvf.name,
            nf=count,
            user=nvf.operator.name,
            code=script.script.replace('\n', '\n        '),
        )
        elements += element
        count += 1

    return [count, elements]


def add_launch(user, nvf, type):
    elements = ""
    num = 0

    element = Template(u'''\
{{name}}_launch:
    type: OS::Heat::SoftwareConfig
    properties:
      group: ungrouped
      config: |
        #!/bin/sh
        cd /home/{{user}}
{{script}}

  ''')
    script = "        "
    if type == "bbu":
        code = nvf.vnf.launch_script.replace("{{user}}", nvf.operator.name) \
            .replace("{{password}}", nvf.operator.password) \
            .replace("{{rrh}}", nvf.rrh.ip) \
            .replace("{{freq}}", str(nvf.freC_DL)) \
            .replace("{{pw}}", str(nvf.pt)) \
            .split("\n")
    for cmd in code:
        script += cmd + "\n        "

    element = element.render(
        name=nvf.name,
        user=user,
        script=script,
    )
    elements += element
    num += 1

    return elements


def add_nvf(ns, nvfs, type):
    elements = ""

    for nvf in nvfs:
        [nfs_num, nfs] = scripts(nvf)
        launch = add_launch(ns.operator.user.username, nvf, type)

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
      availability_zone: nova:{{node}}
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

        if nvf.vnf.create is True:
            image = nvf.vnf.name
        else:
            image = nvf.vnf.image

        t = t.render(
            name=nvf.name,
            image=image,
            flavor=get_flavors(nvf, ns.vim),
            nfs=list_nfs,
            node=ns.vim.select_node(cpu=nvf.vnf.cpu, ram=nvf.vnf.ram, disc=nvf.vnf.disc),
        )
        elements += nfs + launch + t

    return elements


def outputs(nvfs):
    outputs = ""
    for nvf in nvfs:
        output = Template(u'''\
{{name}}_mgmt_ip:
    value: { get_attr: [ {{name}}_floating_ip, floating_ip_address ] }
  {{name}}_id:
    value: { get_resource: {{name}} }
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
        password=ns.operator.decrypt(),
    )

    list_bbus = add_nvf(ns, bbus, "bbu")
    if channels is not None:
        list_channels = add_nvf(ns, channels, "channel")
    if ues is not None:
        list_ues = add_nvf(ns, ues, "ue")

    output = Template(u'''\

outputs:
  ''')
    output = output.render()
    output += outputs(bbus)
    output += outputs(channels)
    output += outputs(ues)

    template = header + list_bbus + list_channels + list_ues + output
    print template
    '''outs = create_stack(name=ns.name,
                       template=template,
                       domain=ns.vim.domain,
                       username=ns.vim.username,
                       project_domain_name=ns.vim.project_domain,
                       project_name=ns.vim.project,
                       password=ns.vim.decrypt(),
                       ip=ns.vim.ip,
                       operator_name=ns.operator.name,
                       operator_password=ns.operator.decrypt())

    print outs

    for out in outs:
        for nvf in bbus:
            if out['output_key'] == nvf.name+"_mgmt_ip":
                nvf.mgmt_ip = out['output_value']
            if out['output_key'] == nvf.name+"_id":
                nvf.uuid = out['output_value']
                nvf.save()
        if channels is not None:
            for nvf in channels:
                if out['output_key'] == nvf.name + "_mgmt_ip":
                    nvf.mgmt_ip = out['output_value']
                if out['output_key'] == nvf.name + "_id":
                    nvf.uuid = out['output_value']
                    nvf.save()
        if ues is not None:
            for nvf in ues:
                if out['output_key'] == nvf.name + "_mgmt_ip":
                    nvf.mgmt_ip = out['output_value']
                if out['output_key'] == nvf.name + "_id":
                    nvf.uuid = out['output_value']
                    nvf.save()'''


def delete_deploy(ns):
    delete_stack(name=ns.name,
                 domain=ns.vim.domain,
                 username=ns.vim.username,
                 project_domain_name=ns.vim.project_domain,
                 project_name=ns.vim.project,
                 password=ns.vim.decrypt(),
                 ip=ns.vim.ip,
                 operator_name=ns.operator.name,
                 operator_password=ns.operator.decrypt())
