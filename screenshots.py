#!/usr/bin/env python

from __future__ import print_function
import urllib
import os
import sys

if __name__=="__main__":
    files = [
        {
            'title': 'oljeproduksjon',
            'filename': '/data/oil_production_yearly_12MMA_mboe_d_by_discovery_decade.csv',
            'unit': 'Millioner fat/dag',
            'output_filename': './img/oil_production_yearly_12MMA_by_discovery_decade.png'
        },
        {
            'title': 'gassproduksjon',
            'filename': '/data/gas_production_yearly_12MMA_mboe_d_by_discovery_decade.csv',
            'unit': 'Millioner fat oljeekvivalenter/dag',
            'output_filename': './img/gas_production_yearly_12MMA_by_discovery_decade.png'
        },
        {
            'title': 'petroleumproduksjon',
            'filename': '/data/oe_production_yearly_12MMA_mboe_d_by_discovery_decade.csv',
            'unit': 'Millioner fat oljeekvivalenter/dag',
            'output_filename': './img/oe_production_yearly_12MMA_by_discovery_decade.png'
        }
    ]
    
    for fil in files:
        url = "http://localhost:8080/bundle?" + urllib.urlencode(fil)
        cmd = "phantomjs screenshot.js \"%s\" %s" % (url, fil['output_filename'])
        print("executing ", cmd, "...")
        ret = os.system(cmd)
        if ret != 0:
            print("executing ", cmd, "... ERROR")
            sys.exit(ret)
        else:
            print("executing ", cmd, "... OK")
