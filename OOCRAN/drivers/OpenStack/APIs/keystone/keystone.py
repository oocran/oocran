from keystoneauth1.identity import v3
from keystoneauth1 import session
import sys
from keystoneclient.v3 import client


def get_session(vim):
    try:
        auth = v3.Password(
                            user_domain_name=vim.domain,
                            username=vim.username,
                            project_domain_name=vim.project_domain,
                            project_name=vim.project,
                            password=vim.password,
                            auth_url="http://"+vim.ip+":5000/v3/")

        sess = session.Session(auth=auth)
        print "Authentification succesfully."
    except:
        print "Authentification failed."
    return sess


def get_token(ns, vim):
     try:
        auth = v3.Password(
                            user_domain_name=vim.domain,
            username=ns.operator.name,
                            project_domain_name=vim.project_domain,
            project_name=ns.operator.name,
            password=ns.operator.password,
                            auth_url="http://"+vim.ip+":5000/v3/")
        sess = session.Session(auth=auth)
        token = auth.get_token(sess)
     except:
         sys.exit(130)
     return token


def get_token_images():
    try:
        auth = v3.Password(
            user_domain_name="default",
            username="admin",
            project_domain_name="default",
            project_name="admin",
            password="odissey09",
            auth_url="http://controller:5000/v3/")
        sess = session.Session(auth=auth)
        token = auth.get_token(sess)
     except:
        sys.exit(130)
     return token


def get_project_id(operator, vim):
    try:
        auth_admin = v3.Password(
                            user_domain_name=vim.domain,
                            username=vim.username,
                            project_domain_name=vim.project_domain,
                            project_name=vim.project,
                            password=vim.password,
                            auth_url="http://"+vim.ip+":35357/v3/")
        sess_admin = session.Session(auth=auth_admin)
        keystone = client.Client(session=sess_admin)
        project = keystone.projects.find(name=operator.user.username)
    except:
         sys.exit(130)
    return project.id


def create_user(operator, vim):
    sess = get_session(vim)
    keystone = client.Client(session=sess)

    project = keystone.projects.find(name=vim.username)

    rol = keystone.roles.find(name="user")
    heat_permi = keystone.roles.find(name="heat_stack_owner")
    project = keystone.projects.create(name=operator.user.username, domain=project.domain_id, enabled=True)
    user = keystone.users.create(name=operator.user.username, password=operator.password, project=project, domain=project.domain_id,enabled=True)
    keystone.roles.grant(rol, user=user, project=project)
    keystone.roles.grant(heat_permi, user=user, project=project)


def delete_user(operator, vim):
    sess = get_session(vim)
    keystone = client.Client(session=sess)

    user = keystone.users.find(name=operator.user.username)
    user.delete()
    project = keystone.projects.find(name=operator.user.username)
    project.delete()



