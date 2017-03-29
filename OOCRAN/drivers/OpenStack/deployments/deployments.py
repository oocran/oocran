from jinja2 import Template
from drivers.OpenStack.APIs.heat.heat import create_stack, delete_stack
from drivers.OpenStack.APIs.keystone.keystone import get_token


def create_deploy(nvfi, bbus):
    header = Template(u'''\
heat_template_version: 2015-10-15
description: {{description}}

parameters:
  NetID:
    type: string
    description: Network ID to use for the instance.
    default: 6de45ecf-4aac-4161-bd8c-ce24951ef6d2
resources:
  credentials:
    type: OS::Heat::CloudConfig
    properties:
      cloud_config:
        chpasswd:
          list: |
            ubuntu:ubuntu
          expire: False

  ''')
    header = header.render(
        description=nvfi.description,
        user=nvfi.operator.name,
        password=nvfi.operator.password,
    )

    elements = ""
    num = 0
    for bbu in bbus:
        nvf = Template(u'''\
script_server{{num}}:
    type: OS::Heat::SoftwareConfig
    properties:
      group: ungrouped
      config: |
        #!/bin/sh
        cd /home/ubuntu
        {{script}}


  server{{num}}_init:
    type: OS::Heat::MultipartMime
    properties:
      parts:
      - config: {get_resource: credentials}
      - config: {get_resource: script_server{{num}}}


  server{{num}}:
    type: OS::Nova::Server
    properties:
      name: {{name}}
      image: {{image}}
      flavor: {{flavor}}
      networks:
      - network: network
      user_data_format: RAW
      user_data:
         get_resource: server{{num}}_init

  ''')

        if bbu.bw_dl == 1400000:
            f = 6
        if bbu.bw_dl == 3000000:
            f = 3

        script = ""
        for nf in bbu.vnf.nf.all():
            script = script + nf.script

        nvf = nvf.render(
            name=bbu.rrh.name,
            image=bbu.vnf.image,
            net=bbu.rrh.place,
            flavor="small",
            num=num,
            # script=str(bbu.vnf.script).replace('\n', '').replace('\r', ';').replace('{{ip}}',bbu.name.split('-')[1]).replace('{{pt}}',str(bbu.pt)).replace('{{freC}}',str(bbu.freC_DL)).replace('{{BW}}',str(f)),
            script=script,
        )
        elements = elements + nvf
        num = num + 1

    template = header+elements
    print template
    create_stack(nvfi, template, nvfi.scenario.vim)


def delete_deploy(nvfi):
    delete_stack(nvfi, nvfi.scenario.vim)