from jinja2 import Template
from drivers.OpenStack.APIs.nova.nova import get_flavors
from vims.models import OpenStack, Aws, Gce, Azure


def libvirt(nvf):
    element = Template(u'''\
  config.vm.synced_folder '.', '/vagrant', type: 'rsync'
  config.vm.define "{{name}}" do |subconfig|
    subconfig.vm.network "private_network", ip: "192.168.50.4"
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
    subconfig.vm.network "private_network", ip: "192.168.50.4"
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
      v.remains_running = true
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


def openstack_v3(nvf):
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

  vim = OpenStack.objects.get(name=nvf.vim.name)

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

''')

  vim = Aws.objects.get(name=nvf.vim.name)

  element = element.render(
      name=nvf.name,
      username=nvf.operator.name,
      image=nvf.vnf.image,
      key=vim.access_key_id,
      secret_key=vim.decrypt(),
      token=vim.session_token,
      keypair=vim.keypair_name,
  )
  return element


def gce(nvf):
  element = Template(u'''\
  config.vm.box = "{{image}}"

  config.vm.provider :google do |google, override|
    google.google_project_id = {{google_project_id}}
    google.google_client_email = {{google_client_email}}
    google.google_json_key_location = {{google_json_key_location}}

    override.ssh.username = {{username}}

''')

  vim = Gce.objects.get(name=nvf.vim.name)

  element = element.render(
      name=nvf.name,
      username=nvf.operator.name,
      image=nvf.vnf.image,
      google_project_id=vim.google_project_id,
      google_client_email=vim.google_client_email,
      google_json_key_location=vim.google_json_key_location,
  )
  return element


def azure(nvf):
  element = Template(u'''\
  config.vm.box = 'azure'

  config.vm.provider :azure do |azure, override|
    azure.tenant_id = {{tenant_id}}
    azure.client_id = {{client_id}}
    azure.client_secret = {{client_secret}}
    azure.subscription_id = {{subscription_id}}

    azure.vm_image_urn = '{{image}}'
    azure.vm_password = {{password}}
    azure.admin_username = {{username}}

''')

  vim = Azure.objects.get(name=nvf.vim.name)

  element = element.render(
      name=nvf.name,
      username=nvf.operator.name,
      password=nvf.operator.decrypt(),
      image=nvf.vnf.image,
      tenant_id=vim.tenant_id,
      client_id=vim.client_id,
      client_secret=vim.decrypt(),
      subscription_id=vim.subscription_id,
  )
  return element
