from jinja2 import Template
from drivers.OpenStack.APIs.nova.nova import get_flavors
from vims.models import OpenStack


def libvirt(nvf):
    element = Template(u'''\
  config.vm.synced_folder '.', '/vagrant', type: 'rsync'
  config.vm.define "{{name}}" do |subconfig|
    subconfig.vm.box = "{{image}}"
    subconfig.vm.provider "libvirt" do |v|
      v.driver = "kvm"
      v.memory = {{ram}}
      v.cpus = {{cpu}}
    end

''')

    element = element.render(
        name=nvf.name,
        image=nvf.vnf.image,
        cpu=nvf.vnf.cpu,
        ram=nvf.vnf.ram,
    )
    return element


def virtualbox(nvf):
    element = Template(u'''\
  config.vm.define "{{name}}" do |subconfig|
    subconfig.vm.network "private_network", ip: "{{ip}}"
    subconfig.vm.box = "{{image}}"
    subconfig.vm.provider "virtualbox" do |v|
      v.memory = {{ram}}
      v.cpus = {{cpu}}
    end

''')

    element = element.render(
        name=nvf.name,
        username = nvf.operator.name,
        password = nvf.operator.decrypt(), 
        image=nvf.vnf.image,
        cpu=nvf.vnf.cpu,
        ram=nvf.vnf.ram,
        ip=nvf.mgmt_ip,
    )
    return element


def docker(nvf):
    element = Template(u'''\
  config.vm.define "{{name}}" do |subconfig|
    subconfig.vm.provider "docker" do |v|
      v.image = "{{image}}"
      v.remains_running = false
    end

''')

    element = element.render(
        name=nvf.name,
        image = nvf.vnf.image,
        cpu=nvf.vnf.cpu,
        ram=nvf.vnf.ram,
        ip=nvf.mgmt_ip,
    )
    return element


def vmware_fusion(nvf):
    element = Template(u'''\
  config.vm.define "{{name}}" do |subconfig|
    subconfig.vm.box = "{{image}}"
    subconfig.vm.provider "vmware_fusion" do |v|
      v.memory = {{ram}}
      v.cpus = {{cpu}}
    end

''')

    element = element.render(
        name=nvf.name,
        image=nvf.vnf.image,
        cpu=nvf.vnf.cpu,
        ram=nvf.vnf.ram,
    )
    return element


def vmware_workstation(nvf):
    element = Template(u'''\
  config.vm.define "{{name}}" do |subconfig|
    subconfig.vm.box = "{{image}}"
    subconfig.vm.provider "vmware_workstation" do |v|
      v.memory = {{ram}}
      v.cpus = {{cpu}}
    end

''')

    element = element.render(
        name=nvf.name,
        image=nvf.vnf.image,
        cpu=nvf.vnf.cpu,
        ram=nvf.vnf.ram,
    )
    return element


def parallels(nvf):
    element = Template(u'''\
  config.vm.define "{{name}}" do |subconfig|
    subconfig.vm.box = "{{image}}"
    subconfig.vm.provider "parallels" do |v|
      v.memory = {{ram}}
      v.cpus = {{cpu}}
    end

''')

    element = element.render(
        name=nvf.name,
        image=nvf.vnf.image,
        cpu=nvf.vnf.cpu,
        ram=nvf.vnf.ram,
    )
    return element


def openstack_v3(nvf, vim):
  element = Template(u'''\
  config.vm.define "{{name}}" do |subconfig|
    subconfig.ssh.username = '{{username}}'  
    subconfig.vm.provider :openstack do |os|
      os.identity_api_version             = '3'
      os.openstack_auth_url               = '{{auth}}'
      os.project_name                     = '{{project}}'
      os.domain_name                      = '{{domain}}'
      os.username                         = '{{username}}'
      os.password                         = '{{password}}'
      os.floating_ip_pool                 = '{{floating}}'
      os.flavor                           = '{{flavor}}'
      os.image                            = '{{image}}'
      os.networks                        << '{{network}}'
    end

    subconfig.vm.define '{{name}}' do |s|
      s.vm.provider :openstack do |os, override|
        os.server_name = '{{name}}'
      end
    end

''')

  vim = OpenStack.objects.get(name=vim.name)

  element = element.render(
      name=nvf.name,
      auth="http://"+vim.ip+":5000/v3",
      tenant=nvf.operator.name,
      username=nvf.operator.name,
      password=nvf.operator.decrypt(),
      floating=vim.public_network,
      domain=vim.domain,
      project=nvf.operator.name,
      flavor=get_flavors(nvf, vim),
      image=nvf.vnf.image,
      network="network",

  )
  return element


def aws(nvf):
  element = Template(u'''\
  config.vm.provider :aws do |aws, override|
    aws.access_key_id = "{{key}}"
    aws.secret_access_key = "{{secret_key}}"
    aws.session_token = "{{token}}"
    aws.keypair_name = "{{keypair}}"
    aws.ami = "{{image}}"
    override.ssh.username = "{{username}}"
  end

''')

  element = element.render(
      name=nvf.name,
      username=nvf.operator.name,
      image=nvf.vnf.image,
      key="",
      secret_key="",
      token="",
      keypair="",
  )
  return element
