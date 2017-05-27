#!/usr/bin/env bash

# MISCELANEOUS
sudo apt-get install g++ python-dev autotools-dev libicu-dev build-essential libbz2-dev -y
sudo apt-get install libusb-1.0-0-dev python-mako doxygen python-docutils cmake git -y
sudo apt-get install libfftw3-dev libfftw3-doc pkg-config -y

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

# CLEAR CACHE
echo "echo 1 > /proc/sys/vm/drop_caches"