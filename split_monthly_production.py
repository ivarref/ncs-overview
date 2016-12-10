#!/usr/bin/env python3

import csv
import os
import codecs

import pandas as pd

if __name__=="__main__":
  frame = pd.read_csv('./data/raw_production_monthly_field.csv')
  names = frame[u'prfInformationCarrier'].unique()
  
  try:
    os.mkdir('./data/fields')
  except:
    pass

  for name in names:
    fil = './data/fields/' + name.replace('/', '%2F') + '.csv'
    print("writing", fil)
    with codecs.open('./data/raw_production_monthly_field.csv', mode='rb', encoding='utf8') as fd:
      reader = csv.reader(fd)
      with open(fil, mode='w', encoding='utf8') as wfd:
        writer = csv.writer(wfd, lineterminator='\n')
        row_to_idx = {}
        for (row_idx, row) in enumerate(reader):
          if row_idx == 0:
            row_to_idx = dict([(k, idx) for (idx, k) in enumerate(row)])
            writer.writerow([x for x in row])
          elif row[row_to_idx[u'prfInformationCarrier']] == name:
            writer.writerow([x for x in row])
          
#    f = frame[frame[u'prfInformationCarrier'] == name]
 #   f.to_csv(fil, line_terminator='\n')
 #   print("generated", fil)
