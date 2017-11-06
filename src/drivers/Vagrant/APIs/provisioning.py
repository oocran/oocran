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

from jinja2 import Template
import os


def script(script):
    element = Template(u'''\
    subconfig.vm.provision "shell", path: "{{file}}"

''')

    element = element.render(
        file=script.filename(),
    )
    return element


def ansible(script):
    element = Template(u'''\
    subconfig.vm.provision "ansible" do |ansible|
      ansible.playbook = "{{file}}"
      ansible.extra_vars = {
        ansible_python_interpreter: "/usr/bin/python3.5",
      }
    end

''')

    element = element.render(
        file=script.filename(),
    )

    return element


def file(script):
    element = Template(u'''\
    subconfig.vm.provision "file", source: "{{file}}", destination: "{{name}}"

''')

    element = element.render(
        file=script.filename(),
        name=str(script.file).split('/')[2]
    )

    return element


def chef(script):
    element = Template(u'''\
    subconfig.vm.provision "chef_apply" do |chef|
      chef.recipe = File.read("{{file}}")
    end

''')

    element = element.render(
        file=script.path+script.file,
    )

    return element


def direct_input(script):
    element = Template(u'''\
    subconfig.vm.provision :shell, :inline => "{{code}}"

''')

    element = element.render(
        code=script.script,
    )

    return element


def puppet(script):
    element = Template(u'''\
    subconfig.vm.provision "puppet" do |puppet|
      puppet.manifests_path = "{{path}}"
      puppet.manifest_file = "{{file}}"
    end

''')

    element = element.render(
        file=script.file,
        path=script.path,
    )

    return element


def salt(script):
    element = Template(u'''\
    subconfig.vm.provision :salt do |salt|
      salt.masterless = true
      salt.minion_config = "{{file}}"
      salt.run_highstate = true
    end

''')

    element = element.render(
        file=script.path+script,
    )

    return element