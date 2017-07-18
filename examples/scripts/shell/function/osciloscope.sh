#!/usr/bin/env bash

sudo apt-get install build-essential -y
sudo apt-get install git -y
sudo apt-get install cmake -y

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

uhd_fft --args=addr=192.168.10.2 --freq 2390000000 --samp-rate=2000000 --gain=50 --averaging --avg-alpha=0.5 --ref-scale=10.0