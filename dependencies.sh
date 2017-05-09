#!/usr/bin/env bash

#sudo apt-get update
sudo apt-get install python-pip -y
sudo apt install influxdb-client -y
sudo apt-get install libpq-dev python-dev libxml2-dev libxslt1-dev libldap2-dev libsasl2-dev libffi-dev -y
sudo apt-get install rabbitmq-server -y

#Configure RabbitMQ
sudo rabbitmqctl add_user oocran oocran
sudo rabbitmqctl add_vhost oocran
sudo rabbitmqctl set_permissions -p oocran oocran ".*" ".*" ".*"

#InfluxDB
sudo apt-get install influxdb -y
influx  -execute "CREATE USER admin WITH PASSWORD 'oocran' WITH ALL PRIVILEGES"
