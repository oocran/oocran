#!/usr/bin/env bash


# Make sure only root can run our script
if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

sudo apt-get update
sudo apt-get install python-pip -y
sudo apt-get install mysql-server -y
sudo apt-get install rabbitmq-server -y

#Configure RabbitMQ
sudo rabbitmqctl add_user oocran oocran
sudo rabbitmqctl add_vhost oocran
sudo rabbitmqctl set_permissions -p oocran oocran ".*" ".*" ".*"

#Configuration Mysql
#mysql -u root -p
#CREATE USER 'oocran'@'localhost' IDENTIFIED BY 'oocran';
#GRANT ALL PRIVILEGES ON * . * TO 'oocran'@'localhost';
#FLUSH PRIVILEGES;

#mysql -u oocran -p
#CREATE DATABASE oocran;