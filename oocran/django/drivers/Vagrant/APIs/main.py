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

import os
import shutil
from jinja2 import Template

import vagrant

import providers
import provisioning


def vagrant_launch(ns, bbus, channels, ues):
    """
    Launch a network services
    :param ns:
    :param bbus:
    :param channels:
    :param ues:
    """
    create_vagrantfile(ns=ns, bbus=bbus, channels=channels, ues=ues)
    v = vagrant.Vagrant(os.getcwd() + '/drivers/Vagrant/repository/' + ns.operator.name + '/' + ns.name)
    try:
        v.up()
    except:
        print "creating"


def vagrant_destroy(ns):
    """
    Destroy specific network service
    :param ns:
    :return:
    """
    v = vagrant.Vagrant(os.getcwd() + '/drivers/Vagrant/repository/' + ns.operator.name + '/' + ns.name)
    v.destroy()
    shutil.rmtree(os.getcwd() + '/drivers/Vagrant/repository/' + ns.operator.name + "/" + ns.name)


def vagrant_ssh(script, nvf):
    """
    Reconfigure VNF
    :param script: commands execute on the vnf
    :param nvf: vnf obj
    :return:
    """
    os.system("cd "+os.getcwd()+'/drivers/Vagrant/repository/'+nvf.operator.name+"/"+nvf.ns.name+";vagrant ssh "+nvf.name+" -c '"+script+"'")


def vagrant_destroy_nvf(nvf):
    """
    Destroy specific VNF
    :param nvf:
    :return:
    """
    os.system("cd " + os.getcwd() + '/drivers/Vagrant/repository/' + nvf.operator.name + "/" + nvf.ns.name + ";vagrant destroy -f " + nvf.name)


def vagrant_launch_nvf(nvf):
    os.system("cd " + os.getcwd() + '/drivers/Vagrant/repository/' + nvf.operator.name + "/" + nvf.ns.name + ";vagrant up " + nvf.name)
    print "nvf "+nvf.name+" launched done!"


def list_boxes():
    """
    get vagrant boxes
    :return: list of boxes
    """
    v = vagrant.Vagrant()
    list = []
    for box in v.box_list():
        list.append(box)
    return list


def launch(nvf, ns):
    
    element = Template(u'''\
    subconfig.vm.provision :shell, :inline => "{{code}}"

''')


    if nvf.typ == "bbu":
        code = nvf.vnf.launch_script.replace("{{user}}", nvf.operator.name) \
                                    .replace("{{passw}}", nvf.operator.decrypt()) \
                                    .replace("{{rrh}}", nvf.rrh.ip) \
                                    .replace("{{freq}}", str(nvf.freC_DL)) \
                                    .replace("{{pw}}", str(nvf.pt)) \
                                    .replace("{{next}}",str(nvf.next_nvf))
    elif nvf.typ == "channel":
        code = nvf.vnf.launch_script.replace("{{tx}}", "aaa")
    elif nvf.typ == "ue":
        code = nvf.vnf.launch_script.replace("{{ue}}", "aaa")

    code =code.replace("{{nvf}}", nvf.name) \
              .replace("{{db}}", "ns_"+str(ns.id)) \
              .replace("{{user}}", ns.operator.name) \
              .replace("{{passw}}", nvf.operator.decrypt()) \
              .replace("{{server}}", "192.168.1.117") \


    element = element.render(
        code=code
    )

    return element
    

def provisions(nvf):
    element = ""
    if nvf.vnf.check_scripts() is not False:
        for script in nvf.vnf.get_scripts_order():
            if script.type == "Script":
                element += provisioning.script(script)
            elif script.type == "Direct Input":
                element += provisioning.direct_input(script)
            elif script.type == "Ansible":
                element += provisioning.ansible(script)
            elif script.type == "Puppet":
                element += provisioning.puppet(script)
            elif script.type == "Chef":
                element += provisioning.chef(script)
            elif script.type == "File":
                element += provisioning.file(script)
            elif script.type == "Salt":
                element += provisioning.salt(script)

    return element


def create_nvf(nvf, ns):
    element = ""
    if nvf.vnf.provider == "VirtualBox":
        element = providers.virtualbox(nvf) + provisions(nvf) + launch(nvf, ns)
    elif nvf.vnf.provider == "Libvirt":
        element = providers.libvirt(nvf) + provisions(nvf) + launch(nvf, ns)
    elif nvf.vnf.provider == "Docker":
        element = providers.docker(nvf) + provisions(nvf) + launch(nvf, ns)
    elif nvf.vnf.provider == "OpenStack":
        element = providers.openstack_v3(nvf) + provisions(nvf)
    elif nvf.vnf.provider == "AWS":
        element = providers.aws(nvf) + provisions(nvf)
    elif nvf.vnf.provider == "GCE":
        element = providers.openstack_v3(nvf) + provisions(nvf)
    elif nvf.vnf.provider == "Azure":
        element = providers.azure(nvf) + provisions(nvf)

    end = Template(u'''\
  end

''')
    element += end.render()

    return element


def create_vagrantfile(ns, bbus, channels=None, ues=None):
    try:
        os.mkdir(os.getcwd() + '/drivers/Vagrant/repository/' + ns.operator.name + "/" + ns.name)
    except:
        print "Folder exist."

    header = Template(u'''\
Vagrant.configure("2") do |config|

''')
    header = header.render()

    nvfs = ""
    for element in bbus:
        nvf = create_nvf(nvf=element, ns=ns)
        nvfs += nvf
    if channels is not None:
        for element in channels:
            nvf = create_nvf(nvf=element, ns=ns)
            nvfs += nvf
    if ues is not None:
        for element in ues:
            nvf = create_nvf(nvf=element, ns=ns)
            nvfs += nvf

    end = Template(u'''\
end
''')
    end = end.render()

    print header + nvfs + end

    outfile = open(os.getcwd() + '/drivers/Vagrant/repository/' + ns.operator.name + "/" + ns.name + '/Vagrantfile', 'w')
    outfile.write(header + nvfs + end)
    outfile.close()
