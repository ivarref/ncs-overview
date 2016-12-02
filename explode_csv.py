#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import csv
import json
import os
import sys
import collections

if __name__=="__main__":
  if len(sys.argv) < 3:
    print("usage: ", sys.argv[0], "input.csv", "output.json")
    sys.exit(1)
  fil = sys.argv[1]
  output = sys.argv[2]

  with open(fil, 'rb') as fd:
    reader = csv.reader(fd)
    columns = []
    res = []
    for (row_idx, row) in enumerate(reader):
      if row_idx == 0:
        w = [unicode(cell, 'utf-8') for cell in row]
        columns = w
      else:
        kv = [(k, unicode(cell, 'utf-8')) for (k, cell) in zip(columns, row)]
        res.append(collections.OrderedDict(kv))
    with open(output, 'wb') as fd:
      fd.write(json.dumps(res, indent=4, separators=(',', ': ')).encode('utf-8'))
      