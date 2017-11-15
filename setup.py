###
#    Open Orchestrator Cloud Radio Access Network
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
###

from setuptools import find_packages, setup
from setuptools.command.develop import develop
from setuptools.command.install import install
from subprocess import check_call
import os


class PostDevelop(develop):
    """Post-installation for development mode."""
    def run(self):
        develop.run(self)


class PostInstall(install):
    """Post-installation for installation mode."""
    def run(self):
        path = os.path.dirname(os.path.abspath(__file__))
        os.system("python oocran/install/key.py "+path)
        os.system("./oocran/install/install.sh")
        install.run(self)

setup(
    name='OOCRAN',
    version='4.0.3',
    url='http://www.oocran.dynu.com/',
    author='OOCRAN Team',
    author_email='info@oocran.dynu.com',
    description=('Orchestrator Layer wireless comunications'),
    license='Apache 2',
    packages=find_packages(),
    install_requires=[
        'django==1.9',
        'django-bootstrap-form==3.2.1',
        'numpy==1.11.1',
        'Jinja2==2.8',
        'celery==4.0.2',
        'django-celery==3.1.17',
        'django-celery-results==1.0.1',
        'django-celery-beat==1.0.1',
        'python-openstackclient==2.6.0',
        'python-neutronclient==6.2.0',
        'python-heatclient==1.2.0',
        'python-ceilometerclient==2.4.0',
        'python-vagrant==0.5.14',
        'yapsy==1.11.223',
        'simple-crypt==4.1.7',
        'influxdb',
        'psutil',
        'paramiko',
        'crypto',
        'pycrypto',
        'docker',
        'pycurl'
    ],
    entry_points={
        'console_scripts': [
            'oocran=oocran:main',
        ],
    },
    cmdclass={'install': PostInstall},
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)