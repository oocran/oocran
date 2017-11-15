#!/usr/bin/env bash

sudo apt-get install python-pip -y
sudo apt install influxdb-client -y
sudo apt-get install libpq-dev python-dev libxml2-dev libxslt1-dev libldap2-dev libsasl2-dev libffi-dev -y
sudo apt-get install rabbitmq-server -y
sudo apt-get install libssl-dev libcurl4-openssl-dev -y
sudo apt-get install nfs-kernel-server -y
#InfluxDB
sudo apt-get install influxdb
#Vagrant
sudo apt-get build-dep vagrant ruby-libvirt -y
sudo apt-get install libxslt-dev libxml2-dev libvirt-dev zlib1g-dev ruby-dev -y
#Config
influx  -execute "CREATE USER admin WITH PASSWORD 'admin' WITH ALL PRIVILEGES"
sudo rabbitmqctl set_permissions -p oocran oocran ".*" ".*" ".*"
vagrant plugin install vagrant-openstack-provider
vagrant plugin install vagrant-libvirt
vagrant plugin install vagrant-vbguest
sudo rabbitmqctl add_user oocran oocran
sudo rabbitmqctl add_vhost oocran