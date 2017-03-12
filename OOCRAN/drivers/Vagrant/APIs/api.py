import vagrant
from jinja2 import Template
import os, shutil
import subprocess


def vagrant_launch(nvfi, bbus):
    create_vagrantfile(nvfi, bbus)
    v = vagrant.Vagrant(os.getcwd() + '/drivers/Vagrant/repository/' + nvfi.operator.name + '/' + nvfi.name)
    v.up(provider=bbus[0].vnf.box.split(' - ')[1])


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


def create_vagrantfile(nvfi, bbus):
    output = subprocess.check_output("lspci| grep VGA", shell=True)
    bus = "0x" + output.split(":")[0]
    slot = "0x" + output.split(":")[1].split(".")[0]
    function = "0x" + output.split(" ")[0].split(".")[1]

    header = Template(u'''\
Vagrant.configure("2") do |config|
  # boxes at https://atlas.hashicorp.com/search.
  ''')
    header = header.render()

    nvfs = ""
    for bbu in bbus:
        nvf = Template(u'''\
config.vm.define "{{name}}" do |v|
    v.vm.box = "{{box}}"
    #v.vm.network "private_network", ip: "{{network}}"
  end
  ''')
        nvf = nvf.render(
            box=bbu.vnf.box.split(' - ')[0],
            name=bbu.rrh.name,
            network=bbu.rrh.ip,
        )
        nvfs = nvfs + nvf

    end = Template(u'''\
config.vm.provider "virtualbox" do |v|
    v.memory = {{ram}}
    v.cpus = {{cpu}}
  end

  config.vm.provider "libvirt" do |v|
    v.random_hostname = true
    v.driver = 'kvm'
    v.memory = {{ram}}
    v.cpus = {{cpu}}
    v.kvm_hidden = true
    #v.video_vram = 1024
    #v.pci :bus => '{{bus}}', :slot => '{{slot}}', :function => '{{function}}'
  end

  #Update and upgrade
  config.vm.provision "shell", inline: <<-SHELL
    script
  SHELL
end
  ''')
    end = end.render(
        ram=bbu.vnf.ram,
        cpu=bbu.vnf.cpu,
        script=bbu.vnf.script_vagrant,
        bus=bus,
        slot=slot,
        function=function,
    )

    os.mkdir(os.getcwd() + '/drivers/Vagrant/repository/' + nvfi.operator.name + "/" + nvfi.name)
    outfile = open(os.getcwd() + '/drivers/Vagrant/repository/' + nvfi.operator.name + '/' + nvfi.name + '/Vagrantfile',
                   'w')
    outfile.write(header + nvfs + end)
    outfile.close()
