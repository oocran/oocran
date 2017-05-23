import vagrant
from jinja2 import Template
import os, shutil


def vagrant_launch(ns, bbus):
    create_vagrantfile(ns, bbus)
    v = vagrant.Vagrant(os.getcwd() + '/drivers/Vagrant/repository/' + ns.operator.name + '/' + ns.name)
    try:
        v.up(provider=ns.operator.vagrant_hypervisor)
    except:
        print "creating"


def vagrant_destroy(ns):
    v = vagrant.Vagrant(os.getcwd() + '/drivers/Vagrant/repository/' + ns.operator.name + '/' + ns.name)
    v.destroy()
    shutil.rmtree(os.getcwd() + '/drivers/Vagrant/repository/' + ns.operator.name + "/" + ns.name)


def list_boxes(operator):
    v = vagrant.Vagrant()
    list = []
    for box in v.box_list():
        print box
        if box.provider == operator.vagrant_hypervisor:
            list.append(box)
    return list


def create_nvf(nvf, count, ns, type):
    element = Template(u'''\

  config.vm.define "{{name}}" do |{{name}}|
    {{name}}.vm.box = "{{box}}"

    {{name}}.vm.provider "{{hypervisor}}" do |v|
      v.memory = {{ram}}
      v.cpus = {{cpu}}
    end

    {{name}}.vm.provision "shell", inline: <<-SHELL
      {{script}}
    SHELL
  end
''')
    script = ""
    for nf in nvf.vnf.nf.all():
        if nf.check_libraries() is not False:
            for library in nf.get_libraries_order():
                script += library.script.replace('\n', '\n      ') + '\n      '

        code = nf.script
        if type == "bbu":
            code = code.replace("{{user}}", nvf.operator.name) \
                .replace("{{password}}", nvf.operator.password) \
                .replace("{{rrh}}", nvf.rrh.ip) \
                .replace("{{freq}}", str(nvf.freC_DL)) \
                .replace("{{pw}}", str(nvf.pt))
        cmds = code.split("\n")
        for cmd in cmds:
            script += cmd + "\n      "

    element = element.render(
        box='debian/jessie64',
        name="vnf" + str(count),
        ram=nvf.vnf.min_ram,
        cpu=nvf.vnf.min_cpu,
        hypervisor=ns.operator.vagrant_hypervisor,
        script=script
    )
    return element


def create_vagrantfile(ns, bbus, channels=None, ues=None):
    header = Template(u'''\
Vagrant.configure("2") do |config|
  # boxes at https://atlas.hashicorp.com/search.
      ''')
    header = header.render()

    nvfs = ""
    count = 0
    for element in bbus:
        nvf = create_nvf(element, count, ns, "bbu")
        nvfs += nvf
        count += 1
    if channels is not None:
        for element in channels:
            nvf = create_nvf(element, count, ns, "channel")
            nvfs += nvf
            count += 1
    if ues is not None:
        for element in ues:
            nvf = create_nvf(element, count, ns, "ue")
            nvfs += nvf
            count += 1
    end = Template(u'''\

end''')
    end = end.render()

    print header + nvfs + end

    os.mkdir(os.getcwd() + '/drivers/Vagrant/repository/' + ns.operator.name + "/" + ns.name)
    outfile = open(os.getcwd() + '/drivers/Vagrant/repository/' + ns.operator.name + "/" + ns.name + '/Vagrantfile', 'w')
    outfile.write(header + nvfs + end)
    outfile.close()
