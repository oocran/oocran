from jinja2 import Template


def script(script):
    element = Template(u'''\
    subconfig.vm.provision "shell", path: "{{file}}"

''')

    element = element.render(
        file=script.file,
    )
    return element


def ansible(script):
    element = Template(u'''\
    subconfig.vm.provision "ansible" do |ansible|
      ansible.playbook = "{{file}}"
      ansible.sudo = true
      ansible.limit = "all"
    end

''')

    element = element.render(
        file=script.filename(),
    )

    return element


def file(file):
    element = Template(u'''\
    config.vm.provision "file", source: "{{file}}", destination: "/vagrant"

''')

    element = element.render(
        file=script.file
    )

    return element


def chef():
    return "chef"


def direct_input(script):
    element = Template(u'''\
    subconfig.vm.provision :shell, :inline => "{{code}}"

''')

    element = element.render(
        code=script.script
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


def salt(file):
    element = Template(u'''\
    subconfig.vm.provision :salt do |salt|
      salt.masterless = true
      salt.minion_config = "{{file}}"
      salt.run_highstate = true
    end

''')

    element = element.render(
        file=file,
        path=file.path,
    )

    return element