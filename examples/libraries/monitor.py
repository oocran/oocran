#!/usr/bin/python

'''
    usage: python monitor.py --nvf marti --ip localhost --db oocran --user admin --pass oocran --time 1
'''

import requests
import sys
import psutil
from time import sleep
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-n', '--nvf', help='NVF name', required=True)
parser.add_argument('-i', '--ip', help='The IP of the influxdb instance', required=True)
parser.add_argument('-d', '--db', help='The influx database', required=True)
parser.add_argument('-u', '--user', help='The influxdb user', required=True)
parser.add_argument('-p', '--pass', help='The influx user password', required=True)
parser.add_argument('-t', '--time', help='Delay in seconds between two consecutive updates', required=True)
args = vars(parser.parse_args())

NVF = args['nvf']
IP = args['ip']
DB = args['db']
USER = args['user']
PASSWORD = args['pass']
TIME = float(args['time'])

while True:
    cpu = 'cpu_' + NVF + ' value=%s' % psutil.cpu_percent()
    disk = 'disk_' + NVF + ' value=%s' % psutil.disk_usage('/').percent
    ram = 'ram_' + NVF + ' value=%s' % psutil.virtual_memory().used
    network_in = 'network_in_' + NVF + ' value=%s' % psutil.net_io_counters().bytes_sent
    network_out = 'network_out_' + NVF + ' value=%s' % psutil.net_io_counters().bytes_recv

    print cpu

    r = requests.post("http://%s:8086/write?db=%s" % (IP, DB), auth=(USER, PASSWORD), data=cpu)
    r = requests.post("http://%s:8086/write?db=%s" % (IP, DB), auth=(USER, PASSWORD), data=disk)
    r = requests.post("http://%s:8086/write?db=%s" % (IP, DB), auth=(USER, PASSWORD), data=ram)
    r = requests.post("http://%s:8086/write?db=%s" % (IP, DB), auth=(USER, PASSWORD), data=network_in)
    r = requests.post("http://%s:8086/write?db=%s" % (IP, DB), auth=(USER, PASSWORD), data=network_out)
    if r.status_code != 204:
        print 'Failed to add point to influxdb (%d) - aborting.' % r.status_code
        sys.exit(1)
    sleep(TIME)
