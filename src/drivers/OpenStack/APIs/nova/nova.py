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

from novaclient import client
from drivers.OpenStack.APIs.keystone.keystone import get_session
import uuid


def add_key(key, vim):
    nova = client.Client(2, session=get_session(
        domain=vim.domain,
        username=key.operator.name,
        project_domain_name=vim.project_domain,
        project_name=key.operator.name,
        password=key.operator.decrypt(),
        ip=vim.ip))
    try:
        nova.keypairs.create(key.name, key.public_key)
    except:
        print "cannot add key"


def del_key(key, vim):
    nova = client.Client(2, session=get_session(
        domain=vim.domain,
        username=key.operator.name,
        project_domain_name=vim.project_domain,
        project_name=key.operator.name,
        password=key.operator.decrypt(),
        ip=vim.ip))
    try:
        nova.keypairs.delete(key.name)
    except:
        print "cannot add key"


def get_flavors(nvf, vim):
    nova = client.Client(2, session=get_session(
        domain=vim.domain,
        username=vim.username,
        project_domain_name=vim.project_domain,
        project_name=vim.project,
        password=vim.decrypt(),
        ip=vim.ip))
    try:
        flavor = nova.flavors.find(vcpus=nvf.vnf.cpu, ram=nvf.vnf.ram, disk=nvf.vnf.disc)
    except:
        flavor = nova.flavors.create(name=str(uuid.uuid4()), ram=nvf.vnf.ram, vcpus=nvf.vnf.cpu,
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
        password=vnf.operator.decrypt(),
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
        password=vim.decrypt(),
        ip=vim.ip))

    return nova.hypervisors.list()


def node_state(vim, node, state):
    nova = client.Client(2, session=get_session(
        domain=vim.domain,
        username=vim.username,
        project_domain_name=vim.project_domain,
        project_name=vim.project,
        password=vim.decrypt(),
        ip=vim.ip))

    node = nova.host.get(host_name=node)
    if state == "up":
        node.startup
    elif state == "down":
        node.shutdown


def launch(name, domain, username, project_domain_name, project_name, password, ip):
    try:
        nova = client.Client(2, session=get_session(
            domain=domain,
            username=username,
            project_domain_name=project_domain_name,
            project_name=project_name,
            password=password,
            ip=ip))

        image = nova.images.find(name=name)
        flavor = nova.flavors.find(name="small")
        net = nova.networks.find(label="network")
        nics = [{'net-id': net.id}]
        nova.servers.create(name="vm2", image=image, flavor=flavor, nics=nics)
    finally:
        print("Execution Completed")


def shut_down(uuid, domain, username, project_domain_name, project_name, password, ip):
    nova = client.Client(2, session=get_session(
        domain=domain,
        username=username,
        project_domain_name=project_domain_name,
        project_name=project_name,
        password=password,
        ip=ip))

    servers_list = nova.servers.list()
    server_del = uuid
    server_exists = False

    for s in servers_list:
        if s.id == server_del:
            print("This server %s exists" % server_del)
            server_exists = True
            break
    if not server_exists:
        print("server %s does not exist" % server_del)
    else:
        print("deleting server..........")
        nova.servers.delete(s)
        print("server %s deleted" % server_del)
