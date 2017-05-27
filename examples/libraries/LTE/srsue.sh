#!/bin/bash
# -*- ENCODING: UTF-8 -*-

#######INSTALLATION#####
#sudo apt-get install zip -y
#unzip srsLTE.zip
#cd srsLTE
#chmod 777 install.sh
#.sudo ./ue ue.conf.example
########################

sudo apt-get update -y && sudo apt-get upgrade -y
sudo apt-get install build-essential -y
sudo apt-get install git -y
sudo apt-get install cmake -y
sudo apt-get install libfftw3-dev libfftw3-doc pkg-config -y
sudo apt-get install g++ python-dev autotools-dev libicu-dev build-essential libbz2-dev -y
sudo apt-get install libusb-1.0-0-dev python-mako doxygen python-docutils cmake -y
sudo apt-get install libboost-all-dev libboost-system-dev libboost-test-dev libboost-thread-dev libqwt-dev libqt4-dev -y
sudo apt-get install liborc-0.4 -y
sudo apt-get install libgps-dev -y

#VOLK
git clone https://github.com/gnuradio/volk.git
cd volk
mkdir build
cd build
cmake ../
sudo make install
cd ../..

# Install UHD
git clone git://github.com/EttusResearch/uhd.git
cd uhd/host
sudo rm -r build
mkdir build
cd build
cmake ../
make
make test
sudo make install
sudo ldconfig
cd ../../..
# Test UHD
#uhd_usrp_probe --args="addr=192.168.10.2"

#SRSLTE
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

# PolarSSL/mbed TLS
wget https://tls.mbed.org/download/start/mbedtls-2.4.2-apache.tgz
tar zxvf mbedtls-2.1.3-apache.tgz
cd mbedtls-2.1.3
cmake -DUSE_SHARED_MBEDTLS_LIBRARY=On -G "Unix Makefiles"
make
sudo make install
cd ..

#UE
git clone https://github.com/srsLTE/srsUE.git
cd srsUE
mkdir build
cd build
cmake ../
make
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

# Clean cache