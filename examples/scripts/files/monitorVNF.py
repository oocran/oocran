#!/usr/bin/python

import requests
from time import sleep
import psutil

NVF = 'RX'
IP = '147.83.118.227'
DB = 'rx'
USER = 'admin'
PASSWORD = 'admin'
TIME = 1


while True:

    cpu = 'cpu' + ' value=%s' % psutil.cpu_percent()
    disk = 'disk' + ' value=%s' % psutil.disk_usage('/').percent
    ram = 'ram' + ' value=%s' % psutil.virtual_memory().used

    requests.post("http://%s:8086/write?db=%s" % (IP, DB), auth=(USER, PASSWORD), data=cpu)
    requests.post("http://%s:8086/write?db=%s" % (IP, DB), auth=(USER, PASSWORD), data=disk)
    requests.post("http://%s:8086/write?db=%s" % (IP, DB), auth=(USER, PASSWORD), data=ram)

    sleep(TIME)
