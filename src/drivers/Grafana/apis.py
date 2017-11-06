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