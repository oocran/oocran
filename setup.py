#!/usr/bin/python
import sys, os

if sys.argv[1] == 'install':
    os.system("./oocran install server")
    print 'OOCRAN installed!'
else:
    print 'Order not found!'