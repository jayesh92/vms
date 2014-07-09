# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.provider :virtualbox do |vb|
    vb.gui=true
  end
  config.vm.box = "systers-vms-dev"
  
  # config.vm.box_url = "../box/pc-web-05192014-i386.box"
  config.vm.box_url = "http://54.183.32.240/vagrant/box/systers-vms.box"

  config.vm.network "forwarded_port", guest: 80, host: 8080
  config.vm.network "forwarded_port", guest: 8000, host:8001
  config.vm.network "private_network", ip: "192.168.33.10"
  config.vm.network "public_network"

end
