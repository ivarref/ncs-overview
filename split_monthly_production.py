#!/usr/bin/env python3

import pandas as pd
import os

if __name__=="__main__":
  frame = pd.read_csv('./data/raw_production_monthly_field.csv')
  names = frame[u'prfInformationCarrier'].unique()
  
  try:
    os.mkdir('./data/fields')
  except:
    pass

  for name in names:
    fil = './data/fields/' + name.replace('/', '%2F') + '.csv'
    f = frame[frame[u'prfInformationCarrier'] == name]
    f.to_csv(fil, line_terminator='\n')
    print("generated", fil)
