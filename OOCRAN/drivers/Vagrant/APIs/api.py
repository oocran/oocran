import vagrant
from jinja2 import Template
import os, shutil


def vagrant_launch(nvfi, bbus):
    create_vagrantfile(nvfi, bbus)
    v = vagrant.Vagrant(os.getcwd() + '/drivers/Vagrant/repository/' + nvfi.operator.name + '/' + nvfi.name)
    v.up(provider=nvfi.operator.vagrant_hypervisor)


def vagrant_destroy(nvfi):
    v = vagrant.Vagrant(os.getcwd() + '/drivers/Vagrant/repository/' + nvfi.operator.name + '/' + nvfi.name)
    v.destroy()
    shutil.rmtree(os.getcwd() + '/drivers/Vagrant/repository/' + nvfi.operator.name + "/" + nvfi.name)


def list_boxes(operator):
    v = vagrant.Vagrant()
    list = []
    for box in v.box_list():
        if box.provider == operator.vagrant_hypervisor:
            list.append(box)
    return list


def create_vagrantfile(nvfi, bbus, channels=None, ues=None):
    header = Template(u'''\
Vagrant.configure("2") do |config|
  # boxes at https://atlas.hashicorp.com/search.
      ''')
    header = header.render()

    nvfs = ""
    count = 0
    for element in bbus:
        nvf = Template(u'''\

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
        for nf in element.vnf.nf.all():
            script = script + nf.script + "\n"

        nvf = nvf.render(
            box='debian/jessie64',
            name="vnf" + str(count),
            ram=element.vnf.ram,
            cpu=element.vnf.cpu,
            hypervisor=nvfi.operator.vagrant_hypervisor,
            script=script
        )
        nvfs = nvfs + nvf
        count += 1
    ###############################################################
    if channels is not None:
        for element in channels:
            nvf = Template(u'''\

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
            for nf in element.vnf.nf.all():
                script = script + nf.script + "\n"

            nvf = nvf.render(
                box='debian/jessie64',
                name="vnf" + str(count),
                ram=element.vnf.ram,
                cpu=element.vnf.cpu,
                hypervisor=nvfi.operator.vagrant_hypervisor,
                script=script,
            )
            nvfs = nvfs + nvf
            count += 1
    ###################################################################
    if ues is not None:
        for element in ues:
            nvf = Template(u'''\

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
            for nf in element.vnf.nf.all():
                script = script + nf.script + "\n"

            nvf = nvf.render(
                box='debian/jessie64',
                name="vnf" + str(count),
                ram=element.vnf.ram,
                cpu=element.vnf.cpu,
                hypervisor=nvfi.operator.vagrant_hypervisor,
                script=script,
            )
            nvfs = nvfs + nvf
            count += 1
    end = Template(u'''\

end''')
    end = end.render()

    os.mkdir(os.getcwd() + '/drivers/Vagrant/repository/' + nvfi.operator.name + "/" + nvfi.name)
    outfile = open(os.getcwd() + '/drivers/Vagrant/repository/' + nvfi.operator.name + "/" + nvfi.name + '/Vagrantfile',
                   'w')
    outfile.write(header + nvfs + end)
    outfile.close()
