import vagrant
from jinja2 import Template
import os, shutil


def vagrant_launch(nvfi, bbus):
    create_vagrantfile(nvfi, bbus)
    v = vagrant.Vagrant(os.getcwd() + '/drivers/Vagrant/repository/' + nvfi.operator.name + '/' + nvfi.name)
    v.up(provider='libvirt')


def vagrant_destroy(nvfi):
    v = vagrant.Vagrant(os.getcwd() + '/drivers/Vagrant/repository/' + nvfi.operator.name + '/' + nvfi.name)
    v.destroy()
    shutil.rmtree(os.getcwd() + '/drivers/Vagrant/repository/' + nvfi.operator.name + "/" + nvfi.name)


def list_boxes():
    v = vagrant.Vagrant()
    list = []
    for box in v.box_list():
        list.append(box.name + ' - ' + box.provider)
    return list


def create_vagrantfile(nvfi, bbus, channels=None, ues=None):
    header = Template(u'''\
    Vagrant.configure("2") do |config|
      # boxes at https://atlas.hashicorp.com/search.
      ''')
    header = header.render()

    nvfs = ""
    for element in bbus:
        nvf = Template(u'''\

      config.vm.define "{{name}}" do |{{name}}|
        {{name}}.vm.box = "{{box}}"

        {{name}}.vm.provider "virtualbox" do |v|
          v.memory = {{ram}}
          v.cpus = {{cpu}}
        end

        {{name}}.vm.provider "libvirt" do |v|
          v.random_hostname = true
          v.driver = 'kvm'
          v.memory = {{ram}}
          v.cpus = {{cpu}}
          v.kvm_hidden = true
        end

        {{name}}.vm.provider "vmware_fusion" do |v|
          v.random_hostname = true
          v.driver = 'kvm'
          v.memory = {{ram}}
          v.cpus = {{cpu}}
          v.kvm_hidden = true
        end

        {{name}}.vm.provider "vmware_workstation" do |v|
          v.random_hostname = true
          v.driver = 'kvm'
          v.memory = {{ram}}
          v.cpus = {{cpu}}
          v.kvm_hidden = true
        end

        {{name}}.vm.provider "docker" do |v|
          v.random_hostname = true
          v.driver = 'kvm'
          v.memory = {{ram}}
          v.cpus = {{cpu}}
          v.kvm_hidden = true
        end

        {{name}}.vm.provision "shell", inline: <<-SHELL
          {{script}}
        SHELL
      end

    ''')
        nvf = nvf.render(
            box='debian/jessie64',
            name=element,
            ram=element.vnf.ram,
            cpu=element.vnf.cpu,
            # script=element.vnf.ns,
        )
        nvfs = nvfs + nvf
    ###############################################################
    for element in channels:
        nvf = Template(u'''\

      config.vm.define "{{name}}" do |{{name}}|
        {{name}}.vm.box = "{{box}}"

        {{name}}.vm.provider "virtualbox" do |v|
          v.memory = {{ram}}
          v.cpus = {{cpu}}
        end

        {{name}}.vm.provider "libvirt" do |v|
          v.random_hostname = true
          v.driver = 'kvm'
          v.memory = {{ram}}
          v.cpus = {{cpu}}
          v.kvm_hidden = true
        end

        {{name}}.vm.provider "vmware_fusion" do |v|
          v.random_hostname = true
          v.driver = 'kvm'
          v.memory = {{ram}}
          v.cpus = {{cpu}}
          v.kvm_hidden = true
        end

        {{name}}.vm.provider "vmware_workstation" do |v|
          v.random_hostname = true
          v.driver = 'kvm'
          v.memory = {{ram}}
          v.cpus = {{cpu}}
          v.kvm_hidden = true
        end

        {{name}}.vm.provider "docker" do |v|
          v.random_hostname = true
          v.driver = 'kvm'
          v.memory = {{ram}}
          v.cpus = {{cpu}}
          v.kvm_hidden = true
        end

        {{name}}.vm.provision "shell", inline: <<-SHELL
          {{script}}
        SHELL
      end

    ''')
        nvf = nvf.render(
            box='debian/jessie64',
            name=element,
            ram=element.vnf.ram,
            cpu=element.vnf.cpu,
            # script=element.vnf.ns,
        )
        nvfs = nvfs + nvf
    ###################################################################
    for element in ues:
        nvf = Template(u'''\

      config.vm.define "{{name}}" do |{{name}}|
        {{name}}.vm.box = "{{box}}"

        {{name}}.vm.provider "virtualbox" do |v|
          v.memory = {{ram}}
          v.cpus = {{cpu}}
        end

        {{name}}.vm.provider "libvirt" do |v|
          v.random_hostname = true
          v.driver = 'kvm'
          v.memory = {{ram}}
          v.cpus = {{cpu}}
          v.kvm_hidden = true
        end

        {{name}}.vm.provider "vmware_fusion" do |v|
          v.random_hostname = true
          v.driver = 'kvm'
          v.memory = {{ram}}
          v.cpus = {{cpu}}
          v.kvm_hidden = true
        end

        {{name}}.vm.provider "vmware_workstation" do |v|
          v.random_hostname = true
          v.driver = 'kvm'
          v.memory = {{ram}}
          v.cpus = {{cpu}}
          v.kvm_hidden = true
        end

        {{name}}.vm.provider "docker" do |v|
          v.random_hostname = true
          v.driver = 'kvm'
          v.memory = {{ram}}
          v.cpus = {{cpu}}
          v.kvm_hidden = true
        end

        {{name}}.vm.provision "shell", inline: <<-SHELL
          {{script}}
        SHELL
      end

    ''')
        nvf = nvf.render(
            box='debian/jessie64',
            name=element,
            ram=element.vnf.ram,
            cpu=element.vnf.cpu,
            # script=element.vnf.ns,
        )
        nvfs = nvfs + nvf

    end = Template(u'''\
    end''')
    end = end.render()

    os.mkdir(os.getcwd() + '/drivers/Vagrant/repository/' + nvfi.operator.name + "/" + nvfi.name)
    outfile = open('Vagrantfile', 'w')
    outfile.write(header + nvfs + end)
    outfile.close()
