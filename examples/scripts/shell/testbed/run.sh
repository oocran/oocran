#!/usr/bin/env bash

#Comands BW=1.4MHz, iteration=4,SNR=3,MCS=6
sudo ./pdsch_enodeb -o a.txt -s 10.0 -p 6 -m 6
sudo ./pdsch_ue  -i a.txt -p 6 -r 1234 -N rx -B rx -I 147.83.118.227 -R admin -W admin
#monitor.conf=iterations1, mcs=6


#Comands BW=5MHz,iteration=4,SNR=3,MCS=6
sudo ./pdsch_enodeb -o a.txt -s 3.0 -p 25 -m 6
sudo ./pdsch_ue  -i a.txt -p 25 -r 1234 -N rx -B rx -I 147.83.118.227 -R admin -W admin
#monitor.conf=iterations1, mcs=6