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

from keystoneauth1.identity import v3
from keystoneauth1 import session
from keystoneclient.v3 import client


def get_session(domain, username, project_domain_name, project_name, password, ip):
    try:
        auth = v3.Password(
            user_domain_name=domain,
            username=username,
            project_domain_name=project_domain_name,
            project_name=project_name,
            password=password,
            auth_url="http://" + ip + ":5000/v3/")
        sess = session.Session(auth=auth)
    except:
        print "Authentification failed."
    return sess


def get_token(domain, username, project_domain_name, project_name, password, ip):
     try:
        auth = v3.Password(
            user_domain_name=domain,
            username=username,
            project_domain_name=project_domain_name,
            project_name=project_name,
            password=password,
            auth_url="http://" + ip + ":5000/v3/")
        sess = session.Session(auth=auth)
        token = auth.get_token(sess)
     except:
         print "Authentification failed."
     return token


def get_project_id(domain, username, project_domain_name, project_name, password, ip, operator_name):
    try:
        auth_admin = v3.Password(
            user_domain_name=domain,
            username=username,
            project_domain_name=project_domain_name,
            project_name=project_name,
            password=password,
            auth_url="http://" + ip + ":35357/v3/")
        sess_admin = session.Session(auth=auth_admin)
        keystone = client.Client(session=sess_admin)
        project = keystone.projects.find(name=operator_name)
    except:
        print "Authentification failed."
    return project.id


def create_user(operator, vim):
    sess = get_session(
        domain=vim.domain,
        username=vim.username,
        project_domain_name=vim.project_domain,
        project_name=vim.project,
        password=vim.decrypt(),
        ip=vim.ip)
    keystone = client.Client(session=sess)
    project = keystone.projects.find(name=vim.username)
    rol = keystone.roles.find(name="user")
    heat = keystone.roles.find(name="heat_stack_owner")
    project = keystone.projects.create(name=operator.user.username, domain=project.domain_id, enabled=True)
    user = keystone.users.create(name=operator.user.username, password=operator.decrypt(), project=project, domain=project.domain_id, enabled=True)
    keystone.roles.grant(rol, user=user, project=project)
    keystone.roles.grant(heat, user=user, project=project)


def delete_user(operator, vim):
    sess = get_session(
        domain=vim.domain,
        username=vim.username,
        project_domain_name=vim.project_domain,
        project_name=vim.project,
        password=vim.decrypt(),
        ip=vim.ip)
    keystone = client.Client(session=sess)
    user = keystone.users.find(name=operator.user.username)
    user.delete()
    project = keystone.projects.find(name=operator.user.username)
    project.delete()



