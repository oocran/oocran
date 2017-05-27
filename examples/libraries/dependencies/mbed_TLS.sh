#!/usr/bin/env bash

sudo apt-get install cmake -y


wget https://tls.mbed.org/download/start/mbedtls-2.4.2-apache.tgz
tar zxvf mbedtls-2.1.3-apache.tgz
cd mbedtls-2.1.3
cmake -DUSE_SHARED_MBEDTLS_LIBRARY=On -G "Unix Makefiles"
make
sudo make install
