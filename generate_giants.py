#!/usr/bin/env python3

import csv
import sys

import pandas as pd

import generate

if __name__=="__main__":
  with open('./data/raw_reserves_field_discovery_year_mboe.csv', 'r') as rfd:
    reader = csv.reader(rfd)

    with open('./data/raw_reserves_field_giants_mboe.csv', 'w') as wfd:
      writer = csv.writer(wfd)

      header2idx = {}
      for (idx, row) in enumerate(reader):
        def value(k):
          return row[header2idx[k]]
        
        def floatvalue(k):
          return float(row[header2idx[k]])

        if idx == 0:
          header2idx = dict([(header, idx) for (idx, header) in enumerate(row)])
          writer.writerow(row)
        else:
          if floatvalue('fldRecoverableOE') >= 1000:
            writer.writerow(row)
        pass

    