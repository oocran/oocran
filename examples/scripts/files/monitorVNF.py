#!/usr/bin/python

import requests
from time import sleep
import time
import psutil
import os

NVF = 'test'
IP = '192.168.1.117'
DB = 'ns_1'
USER = 'test'
PASSWORD = 'test'
TIME = 1
interface = "lo"

cpu = 0.0
ul=0.00
dl=0.00
t0 = time.time()
upload=psutil.net_io_counters(pernic=True)[interface][0]
download=psutil.net_io_counters(pernic=True)[interface][1]
up_down=(upload,download)

while True:
    for proc in psutil.process_iter():
        process = psutil.Process(proc.pid)
        pname = process.name()
        if pname == "pdsch_enodeb" or pname == "pdsch_ue":
            percent = process.cpu_percent(interval=0.1)
            if str(percent) != '0.0':
                cpu = 'cpu' + ' value=%s' % percent
                disk = 'disk' + ' value=%s' % psutil.disk_usage('/').percent
                ram = 'ram' + ' value=%s' % round(process.memory_percent(), 2)

                last_up_down = up_down
                upload = psutil.net_io_counters(pernic=True)[interface][0]
                download = psutil.net_io_counters(pernic=True)[interface][1]
                t1 = time.time()
                up_down = (upload, download)
                try:
                    ul, dl = [(now - last) / (t1 - t0) / 1024.0
                              for now, last in zip(up_down, last_up_down)]
                    t0 = time.time()
                except:
                    pass
                if dl > 0.1 or ul >= 0.1:
                    time.sleep(0.75)
                    os.system('cls')
                    #print('UL: {:0.2f} kB/s \n'.format(ul) + 'DL: {:0.2f} kB/s'.format(dl))

                network_in = 'network_in_' + NVF + ' value=%s' % ul
                network_out = 'network_out_' + NVF + ' value=%s' % dl

                requests.post("http://%s:8086/write?db=%s" % (IP, DB), auth=(USER, PASSWORD), data=cpu)
                requests.post("http://%s:8086/write?db=%s" % (IP, DB), auth=(USER, PASSWORD), data=disk)
                requests.post("http://%s:8086/write?db=%s" % (IP, DB), auth=(USER, PASSWORD), data=ram)
                requests.post("http://%s:8086/write?db=%s" % (IP, DB), auth=(USER, PASSWORD), data=network_in)
                requests.post("http://%s:8086/write?db=%s" % (IP, DB), auth=(USER, PASSWORD), data=network_out)

    sleep(TIME)

