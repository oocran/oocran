#!/usr/bin/env bash

sudo apt-get update -y && sudo apt-get upgrade -y
sudo apt-get install build-essential git cmake -y

#VBBU
git clone https://github.com/oocran/vbbu.git
cd vbbu
mkdir build
cd build
cmake ../
sudo make install
sudo chmod +x *
path=$(pwd)
sudo ln -s "$path"/* /usr/bin
cd ../..

# Modify /etc/sysctl.conf
sudo echo 'kernel.msgmnb=209715200' | sudo tee -a /etc/sysctl.conf
sudo echo 'kernel.msgmax=10485760' | sudo tee -a /etc/sysctl.conf
sudo echo 'net.core.rmem_max=50000000' | sudo tee -a /etc/sysctl.conf
sudo echo 'net.core.wmem_max=1048576' | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
user=$(whoami)
sudo echo "$user        -       rtprio     99" | sudo tee -a /etc/security/limits.conf
sudo echo "$user        -       memlock    unlimited" | sudo tee -a /etc/security/limits.conf
sudo cat /etc/security/limits.conf