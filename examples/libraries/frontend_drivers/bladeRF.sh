#!/usr/bin/env bash

sudo apt-get install build-essential -y
sudo apt-get install git -y
sudo apt-get install cmake -y
sudo apt-get install libusb-1.0-0 -y

git clone https://github.com/Nuand/bladeRF.git
mkdir -p build
cd build
cmake ../
make
sudo make install
sudo ldconfig