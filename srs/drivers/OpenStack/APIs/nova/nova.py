from novaclient import client
from drivers.OpenStack.APIs.keystone.keystone import get_session
import uuid


def get_flavors(nvf, vim):
    nova = client.Client(2, session=get_session(
        domain=vim.domain,
        username=vim.username,
        project_domain_name=vim.project_domain,
        project_name=vim.project,
        password=vim.password,
        ip=vim.ip))
    try:
        flavor = nova.flavors.find(vcpus=nvf.vnf.min_cpu, ram=nvf.vnf.min_ram, disk=nvf.vnf.disc)
    except:
        flavor = nova.flavors.create(name=str(uuid.uuid4()), ram=nvf.vnf.min_ram, vcpus=nvf.vnf.min_cpu,
                                     disk=nvf.vnf.disc, flavorid='auto', ephemeral=0, swap=0, rxtx_factor=1.0,
                                     is_public=True)
        flavor.set_keys(nvf.vnf.extra_spec())
    return flavor.name


def create_snapshot(vnf, vim):
    nova = client.Client(2, session=get_session(
        domain=vim.domain,
        username=vnf.operator.name,
        project_domain_name=vim.project_domain,
        project_name=vnf.operator.name,
        password=vnf.operator.password,
        ip=vim.ip))
    server = nova.servers.find(name=vnf.name)
    nova.servers.create_image(server, vnf.name)
    print "Snapshot created!!"


def log(name, domain, username, project_domain_name, project_name, password, ip):
    nova = client.Client(2, session=get_session(
        domain=domain,
        username=username,
        project_domain_name=project_domain_name,
        project_name=project_name,
        password=password,
        ip=ip))

    server = nova.servers.find(name=name)
    return nova.servers.get_console_output(server)


def console(name, domain, username, project_domain_name, project_name, password, ip):
    nova = client.Client(2, session=get_session(
        domain=domain,
        username=username,
        project_domain_name=project_domain_name,
        project_name=project_name,
        password=password,
        ip=ip))

    server = nova.servers.find(name=name)
    return nova.servers.get_vnc_console(server, "novnc")


def get_hypervisors(vim):
    nova = client.Client(2, session=get_session(
        domain=vim.domain,
        username=vim.username,
        project_domain_name=vim.project_domain,
        project_name=vim.project,
        password=vim.password,
        ip=vim.ip))

    return nova.hypervisors.list()


def node_state(vim, node, state):
    nova = client.Client(2, session=get_session(
        domain=vim.domain,
        username=vim.username,
        project_domain_name=vim.project_domain,
        project_name=vim.project,
        password=vim.password,
        ip=vim.ip))

    node = nova.host.get(host_name=node)
    if state == "up":
        node.startup
    elif state == "down":
        node.shutdown
