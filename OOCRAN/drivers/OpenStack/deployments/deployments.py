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
  ''')
    header = header.render(
        description=nvfi.description,
    )

    elements = ""
    num = 0
    for bbu in bbus:
        nvf = Template(u'''\
server{{num}}:
    type: OS::Nova::Server
    properties:
      name: {{name}}
      image: {{image}}
      flavor: {{flavor}}
      networks:
      - network: {{net}}_bbu_net
      user_data_format: RAW
      user_data: |
        #cloud-config
        runcmd:
         - echo "{{script}}" >> /home/nodea/start.sh
         - sh /home/nodea/start.sh

  ''')

        if bbu.bw_dl == 1400000:
            f = 6
        if bbu.bw_dl == 3000000:
            f = 3

        nvf = nvf.render(
            name=bbu.rrh.name,
            image=bbu.vnf.image,
            net=bbu.rrh.place,
            flavor=bbu.vnf.flavor,
            num=num,
            script=str(bbu.vnf.script).replace('\n', '').replace('\r', ';').replace('{{ip}}',bbu.name.split('-')[1]).replace('{{pt}}',str(bbu.pt)).replace('{{freC}}',str(bbu.freC_DL)).replace('{{BW}}',str(f)),
        )
        elements = elements + nvf
        num = num + 1

    template = header+elements

    res = create_stack(nvfi, template, nvfi.scenario.vim)


def delete_deploy(nvfi):
    print "deleted"
    delete_stack(nvfi, nvfi.scenario.vim)


def create_gui(NVFI, elements, connections):
    template = ""

    header = Template(u'''\
heat_template_version: 2015-10-15
description: {{description}}

parameters:
  NetID:
    type: string
    description: Network ID to use for the instance.
    default: 6de45ecf-4aac-4161-bd8c-ce24951ef6d2
resources:
  ''')
    header = header.render(
        description=NVFI.description,
    )
    template = template+header

    for link in connections:
        net = Template(u'''\
net{{link}}:
    type: OS::Neutron::Net
    properties:
      name: net_{{link}}

  subnet{{link}}:
    type: OS::Neutron::Subnet
    properties:
      name: subnet_{{link}}
      network_id: { get_resource: net{{link}} }
      cidr: {{cidr}}
  ''')
        net = net.render(
            link=link,
            cidr="10.0.0.0/24",
        )
        template = template + net

    num = 0
    for element in elements:
        nvf = Template(u'''\
server{{num}}:
    type: OS::Nova::Server
    properties:
      name: {{name}}
      image: {{image}}
      flavor: {{flavor}}
      networks:
      - network: { get_resource: netid_-2 }
      user_data_format: RAW
      user_data: |
        #cloud-config
        runcmd:
         - echo "{{script}}" >> /home/nodea/start.sh
         - sh /home/nodea/start.sh
  ''')
        nvf = nvf.render(
            name=element,
            image="UBU1404SERVER6GUHD380srsLTE_AUTOSTART",
            flavor="m1.small",
            script="small",
            num=num
        )
        template += nvf
        num+=1

    res = create_stack(NVFI.name, template, NVFI.scenario, NVFI.operator)
    return res