#!/usr/bin/env python3

import csv
import sys

import pandas as pd

import generate

if __name__=="__main__":
  frame = pd.read_csv('./data/raw_discovery_overview.csv')
  ignore = pd.read_csv('./data/ignore_discovery.csv')

  with open('./data/raw_discovery_resources.csv', 'r') as rfd:
    reader = csv.reader(rfd)
    colname2idx = {}
    for (idx, row) in enumerate(reader):
      if idx==0:
        if row[0] != 'dscName':
          print("format changed, expected dscName for first column, was", row[0])
          sys.exit(1)
        header = [row[0], 'dscDiscoveryYear'] + row[1:]
        colname2idx = dict([(colname, idx) for (idx, colname) in enumerate(row)])
        print(*header,sep=',')
      else:
        dscNpdidDiscovery = int(row[colname2idx['dscNpdidDiscovery']])
        dscDiscoveryYear = frame[frame.dscNpdidDiscovery == dscNpdidDiscovery].dscDiscoveryYear.tolist()
        if len(dscDiscoveryYear) == 0:
          if len(ignore[ignore.dscNpdidDiscovery == dscNpdidDiscovery].dscDiscoveryYear.tolist())==1:
            continue
          else:
            print("cannot ignore row", row)
            sys.exit(1)
        elif len(dscDiscoveryYear) >1:
          print("cannot ignore row", row)
          sys.exit(1)
        elif len(dscDiscoveryYear)==1:
          row = [row[0], dscDiscoveryYear[0]] + row[1:]
          print(*row,sep=',')
        else:
          print('abort')
          sys.exit(1)