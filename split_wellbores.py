#!/usr/bin/env python3

import codecs
import collections
import csv
import json
import math
import os
import urllib.parse

import pandas as pd

if __name__=="__main__":
  frame = pd.read_csv('./data/raw_wellbore.csv')
  names = [x for x in frame[u'wlbWellboreName'].unique() if not type(x) == float]
  

  #for (idx, name) in enumerate(names):
  #  fil = './data/wellbores/' + urllib.parse.quote(name, safe='') + '.json'
  #  print("writing", fil, " ...", idx+1, "of", len(names))
  with codecs.open('./data/raw_wellbore.csv', mode='rb', encoding='utf8') as fd:
    reader = csv.reader(fd)
    #with open(fil, mode='w', encoding='utf8') as wfd:
    idx_to_col = {}
    col_to_idx = {}
    for (row_idx, row) in enumerate(reader):
      if row_idx == 0:
        col_to_idx = dict([(k, idx) for (idx, k) in enumerate(row)])
        idx_to_col = dict([(idx, k) for (idx, k) in enumerate(row)])
      else:
        # row[col_to_idx[u'wlbWellboreName']] == name:
        name = row[col_to_idx[u'wlbWellboreName']]
        entryYear = row[col_to_idx[u'wlbEntryYear']]
        int(entryYear)
        try:
          os.makedirs('./data/wellbores/' + entryYear)
        except:
          pass

        vals = [(idx_to_col[idx], val) for (idx, val) in enumerate(row)]
        d = collections.OrderedDict(vals)
        print("writing", name, "with entryYear", entryYear)
        fil = './data/wellbores/' + entryYear + '/' + urllib.parse.quote(name, safe='') + '.json'
        with open(fil, 'w') as wfd:
          json.dump(d, wfd, indent=2)

