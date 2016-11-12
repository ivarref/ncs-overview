#!/usr/bin/env python

from __future__ import print_function
import os
import sys

if __name__=="__main__":
    files = {
        'oil': './img/oil_production_yearly_12MMA_by_discovery_decade.png',
        'gas': './img/gas_production_yearly_12MMA_by_discovery_decade.png',
        'petroleum': './img/oe_production_yearly_12MMA_by_discovery_decade.png'
    }
    for (mode, fil) in files.items():
        url = "http://localhost:8080/bundle?mode=" + mode
        cmd = "phantomjs screenshot.js \"%s\" %s" % (url, fil)
        print("executing ", cmd, "...")
        ret = os.system(cmd)
        if ret != 0:
            print("executing ", cmd, "... ERROR")
            sys.exit(ret)
        else:
            print("executing ", cmd, "... OK")
