#!/usr/bin/env bash

# BOOST
sudo apt-get install libboost-all-dev libboost-system-dev libboost-test-dev libboost-thread-dev libqwt-dev libqt4-dev -y
sudo apt-get install build-essential git cmake -y
sudo apt-get install libfftw3-dev libfftw3-doc pkg-config -y
#VOLK
sudo apt-get install liborc-0.4 -y
sudo apt-get install libgps-dev -y
git clone https://github.com/gnuradio/volk.git
cd volk
mkdir build
cd build
cmake ../
sudo make install
cd ../..

# CLEAR CACHE
echo "echo 1 > /proc/sys/vm/drop_caches"