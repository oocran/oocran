#!/usr/bin/python

import requests
import sys
import psutil
from time import sleep

NVF = "bbu"  # NVF name
IP = "localhost"  # The IP of the influxdb instance
DB = "oocran"  # The influx database
USER = "admin"  # The influxdb user
PASSWORD = "oocran"  # The influx user password
TIME = 1  # Delay in seconds between two consecutive updates

while True:
    cpu = 'cpu value=%s' % psutil.cpu_percent()
    disk = 'disk value=%s' % psutil.disk_usage('/')
    ram = 'ram value=%s' % psutil.virtual_memory()

    r = requests.post("http://%s:8086/write?db=%s" % (IP, DB), auth=(USER, PASSWORD), data=cpu)
    if r.status_code != 204:
        print 'Failed to add point to influxdb (%d) - aborting.' % r.status_code
        sys.exit(1)
    sleep(TIME)
