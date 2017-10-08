#!/usr/bin/env bash

echo "Install OOCRAN dependencies!"
echo ""
cd /tmp
#sudo apt-get update
sudo apt-get install python-pip -y
sudo apt install influxdb-client -y
sudo apt-get install libpq-dev python-dev libxml2-dev libxslt1-dev libldap2-dev libsasl2-dev libffi-dev -y
sudo apt-get install rabbitmq-server -y
sudo apt-get install libssl-dev libcurl4-openssl-dev python-dev -y
sudo apt-get install nfs-kernel-server -y
#InfluxDB
sudo apt-get install influxdb
#Vagrant
sudo apt-get build-dep vagrant ruby-libvirt -y
sudo apt-get install qemu libvirt-bin ebtables dnsmasq -y
sudo apt-get install libxslt-dev libxml2-dev libvirt-dev zlib1g-dev ruby-dev -y
sudo apt-get install vagrant -y