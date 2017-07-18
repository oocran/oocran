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
#InfluxDB
wget https://dl.influxdata.com/influxdb/releases/influxdb_1.2.4_amd64.deb
sudo dpkg -i influxdb_1.2.4_amd64.deb
rm influxdb_1.2.4_amd64.deb
influx  -execute "CREATE USER admin WITH PASSWORD 'admin' WITH ALL PRIVILEGES"
#Kapacitor
wget https://dl.influxdata.com/kapacitor/releases/kapacitor_1.3.1_amd64.deb
sudo dpkg -i kapacitor_1.3.1_amd64.deb
rm kapacitor_1.3.1_amd64.deb
#Grafana
wget https://s3-us-west-2.amazonaws.com/grafana-releases/release/grafana_4.3.2_amd64.deb
sudo apt-get install -y adduser libfontconfig
sudo dpkg -i grafana_4.3.2_amd64.deb
rm grafana_4.3.2_amd64.deb
#Configure RabbitMQ
sudo rabbitmqctl add_user oocran oocran
sudo rabbitmqctl add_vhost oocran
sudo rabbitmqctl set_permissions -p oocran oocran ".*" ".*" ".*"
#Vagrant
sudo apt-get build-dep vagrant ruby-libvirt -y
sudo apt-get install qemu libvirt-bin ebtables dnsmasq -y
sudo apt-get install libxslt-dev libxml2-dev libvirt-dev zlib1g-dev ruby-dev -y
vagrant plugin install vagrant-openstack-provider 
vagrant plugin install vagrant-libvirt