import vagrant
import providers, provisioning
from jinja2 import Template
import os, shutil
from django.contrib.sites.shortcuts import get_current_site


def vagrant_launch(ns, bbus, channels, ues):
    create_vagrantfile(ns=ns, bbus=bbus, channels=channels, ues=ues)
    v = vagrant.Vagrant(os.getcwd() + '/drivers/Vagrant/repository/' + ns.operator.name + '/' + ns.name)
    try:
        v.up()
    except:
        print "creating"


def vagrant_destroy(ns):
    v = vagrant.Vagrant(os.getcwd() + '/drivers/Vagrant/repository/' + ns.operator.name + '/' + ns.name)
    v.destroy()
    shutil.rmtree(os.getcwd() + '/drivers/Vagrant/repository/' + ns.operator.name + "/" + ns.name)


def vagrant_ssh(script, nvf):
    os.system("cd "+os.getcwd()+'/drivers/Vagrant/repository/'+nvf.operator.name+"/"+nvf.ns.name+";vagrant ssh "+nvf.name+" -c '"+script+"'")
    print "reconfiguration done!"


def vagrant_destroy_nvf(nvf):
    os.system("cd " + os.getcwd() + '/drivers/Vagrant/repository/' + nvf.operator.name + "/" + nvf.ns.name + ";vagrant destroy -f " + nvf.name)
    print "nvf shut down done!"


def vagrant_launch_nvf(nvf):
    os.system("cd " + os.getcwd() + '/drivers/Vagrant/repository/' + nvf.operator.name + "/" + nvf.ns.name + ";vagrant up " + nvf.name)
    print "nvf "+nvf.name+" launched done!"


def list_boxes():
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
                                    .replace("{{password}}", nvf.operator.decrypt()) \
                                    .replace("{{rrh}}", nvf.rrh.ip) \
                                    .replace("{{freq}}", str(nvf.freC_DL)) \
                                    .replace("{{pw}}", str(nvf.pt)) \
                                    .replace("{{next}}",str(nvf.next_nvf))
    elif nvf.typ == "channel":
        code = nvf.vnf.launch_script.replace("{{tx}}", "aaa")
    elif nvf.typ == "ue":
        code = nvf.vnf.launch_script.replace("{{ue}}", "aaa")

    print 

    code =code.replace("{{nvf}}", nvf.name) \
              .replace("{{oocran}}", "192.168.10.108") \
              .replace("{{db}}", "ns_"+str(ns.id)) \
              .replace("{{user}}", ns.operator.name) \
              .replace("{{password}}", nvf.operator.decrypt()) \
              .replace("{{interface}}", "eth0")

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
        element = providers.openstack_v3(nvf, nvf.vim) + provisions(nvf)

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
