from urllib import urlencode
import pycurl, json
from StringIO import StringIO
from oocran import settings


def create_user(admin, operator):
    c = pycurl.Curl()
    c.setopt(c.URL, 'http://'+admin.name+':'+admin.decrypt()+'@'+settings.GRAFANA+'/api/admin/users')
    post_data = {'name': operator.name,
                 'email': operator.email,
                 'login': operator.name,
                 'password': operator.decrypt()}
    postfields = urlencode(post_data)
    c.setopt(c.POSTFIELDS, postfields)
    c.perform()
    c.close()


def delete_user(admin, operator):
    c = pycurl.Curl()
    c.setopt(c.URL, 'http://'+admin.name+':'+admin.decrypt()+'@'+settings.GRAFANA+'/api/admin/users/'+operator.name)
    c.setopt(pycurl.CUSTOMREQUEST, "DELETE")
    c.perform()
    c.close()


def create_organization(operator):
    c = pycurl.Curl()
    c.setopt(c.URL, 'http://'+operator.name+':'+operator.decrypt()+'@'+settings.GRAFANA+'/api/orgs')
    post_data = {'name': operator.name}
    postfields = urlencode(post_data)
    c.setopt(c.POSTFIELDS, postfields)
    c.perform()
    c.close()


def get_organization_id(admin, operator):
    buffer = StringIO()
    c = pycurl.Curl()
    c.setopt(c.URL, 'http://'+admin.name+':'+admin.decrypt()+'@'+settings.GRAFANA+'/api/orgs/name/'+operator.name)
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()

    body = json.loads(buffer.getvalue())
    return str(body['id'])


def create_data_source(ns):
    c = pycurl.Curl()
    c.setopt(c.URL, 'http://' + ns.operator.name + ':' + ns.operator.decrypt() + '@'+settings.GRAFANA+'/api/datasources')
    post_data = {"name":"ns_"+str(ns.id),
                "type":"influxdb",
                "url":"http://localhost:8086",
                "access":"proxy",
                "basicAuth":"false",
                "database":"ns_"+str(ns.id),
                "user":ns.operator.name,
                "password":ns.operator.decrypt()}
    postfields = urlencode(post_data)
    c.setopt(c.POSTFIELDS, postfields)
    c.perform()
    c.close()


def alert_notification(operator):
    c = pycurl.Curl()
    c.setopt(c.URL, 'http://'+operator.name+':'+operator.decrypt()+'@'+settings.GRAFANA+'/api/alert-notifications')
    post_data = {"name": "oocran",
                "type": "webhook",
                "settings": {
                    "username": "carl"}
                }
    postfields = urlencode(post_data)
    c.setopt(c.POSTFIELDS, postfields)
    c.perform()
    c.close()