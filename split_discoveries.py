#!/usr/bin/env python3

import codecs
import collections
import csv
import json
import math
import os

import pandas as pd

if __name__=="__main__":
  frame = pd.read_csv('./data/raw_discovery_overview_simplified.csv')
  names = [x for x in frame[u'fldName'].unique() if not type(x) == float]
  
  try:
    os.mkdir('./data/discoveries')
  except:
    pass

  for name in names:
    fil = './data/discoveries/' + name.replace('/', '%2F') + '.json'
    print("writing", fil)
    with codecs.open('./data/raw_discovery_overview_simplified.csv', mode='rb', encoding='utf8') as fd:
      reader = csv.reader(fd)
      with open(fil, mode='w', encoding='utf8') as wfd:
        idx_to_col = {}
        col_to_idx = {}
        for (row_idx, row) in enumerate(reader):
          if row_idx == 0:
            col_to_idx = dict([(k, idx) for (idx, k) in enumerate(row)])
            idx_to_col = dict([(idx, k) for (idx, k) in enumerate(row)])
          elif row[col_to_idx[u'fldName']] == name:
            vals = [(idx_to_col[idx], val) for (idx, val) in enumerate(row)]
            d = collections.OrderedDict(vals)
            with open(fil, 'w') as wfd:
              json.dump(d, wfd, indent=2, ensure_ascii=False)
