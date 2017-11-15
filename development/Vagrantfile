Vagrant.configure("2") do |config|
  # boxes at https://atlas.hashicorp.com/search.

  config.vm.define "vm" do |v|
    v.vm.box = "debian/jessie64"
  end

  config.vm.provider "virtualbox" do |v|
    v.memory = 1024
    v.cpus = 1
  end

  config.vm.provider "libvirt" do |v|
    v.random_hostname = true
    v.driver = 'kvm'
    v.memory = 1024
    v.cpus = 1
  end

  #config.vm.synced_folder "/", "/vagrant"

  #Update and upgrade
  config.vm.provision "shell", inline: <<-SHELL
    sudo apt-get update -y
    sudo apt-get install python-pip -y
    sudo apt-get install git -y
    git clone https://github.com/oocran/oocran.git
    cd oocran;chmod +x oocran
    ./oocran install dependencies
    ./oocran install server
    ./oocran start localhost:8000
  SHELL
end