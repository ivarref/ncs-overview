#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import os
import sys

if __name__=="__main__":
  fil = sys.argv[1]
  columns = sys.argv[2:]
  print("dropping columns", columns, "for file", fil)

  if os.path.exists(fil+'.tmp'):
    os.remove(fil+'.tmp')

  with open(fil, 'r') as fd:
    with open(fil+'.tmp', 'w') as wfd:
      reader = csv.reader(fd)
      writer = csv.writer(wfd, lineterminator='\n')
      skip_idx = []
      for (idx, row) in enumerate(reader):
        if idx == 0:
          for (col_idx, cell) in enumerate(row):
            if cell in columns:
              skip_idx.append(col_idx)
          print("dropping columns indexes", skip_idx)
        row_filtered = [cell for (col_idx, cell) in enumerate(row) if col_idx not in skip_idx]
        writer.writerow(row_filtered)
  os.remove(fil)
  os.rename(fil+'.tmp', fil)
