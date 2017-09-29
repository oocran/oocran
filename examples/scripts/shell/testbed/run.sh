#!/usr/bin/env bash

sudo ./pdsch_enodeb -o a.txt -s 10
sudo ./pdsch_ue  -i a.txt -E -N ue1 -B ns_1 -I 192.168.1.117 -R user1 -W user1

#canal
#sudo ./pdsch_enodeb -o aa.txt -p 6 -s 10.0 -m 12
#sudo ./pdsch_ue -r 1234 -p 6 -i aa.txt -E -N ue1 -B ns_1 -I 192.168.1.117 -R user1 -W user1