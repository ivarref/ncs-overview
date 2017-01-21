#!/usr/bin/env python3

import csv
import sys

import pandas as pd

import generate

if __name__=="__main__":
  with open('./data/raw_reserves_field.csv', 'r') as rfd:
    reader = csv.reader(rfd)

    with open('./data/field_percentage_produced.csv', 'w') as wfd:
      writer = csv.writer(wfd)
      with open('./data/field_since_2000_percentage_produced.csv', 'w') as wfd2:
        writer2 = csv.writer(wfd2)

        header2idx = {}
        for (idx, row) in enumerate(reader):
          def value(k):
            return row[header2idx[k]]
          
          def floatvalue(k):
            return float(row[header2idx[k]])

          def percentage(k):
            recoverable = floatvalue('fldRecoverable'+k)
            remaining = floatvalue('fldRemaining'+k)
            produced = recoverable - remaining
            if recoverable == 0:
              return ""
            percentage = (produced*100.0) / recoverable
            return "%.1f" % (percentage)

          if idx == 0:
            header2idx = dict([(header, idx) for (idx, header) in enumerate(row)])
            writer.writerow(['fldName', 'fldDiscoveryYear', 'percentageProducedOil', 'percentageProducedGas', 'percentageProducedOE'])
            writer2.writerow(['fldName', 'fldDiscoveryYear', 'percentageProducedOil', 'percentageProducedGas', 'percentageProducedOE'])
          else:
            newrow = []
            writer.writerow([value('fldName'), value('fldDiscoveryYear'), percentage('Oil'), percentage('Gas'), percentage('OE')])
            if floatvalue('fldDiscoveryYear') >= 2000:
              writer2.writerow([value('fldName'), value('fldDiscoveryYear'), percentage('Oil'), percentage('Gas'), percentage('OE')])
          pass

    for f in ['./data/field_since_2000_percentage_produced.csv', './data/field_percentage_produced.csv']:
      frame = pd.read_csv(f)
      frame.sort_values(by=['percentageProducedOE', 'fldDiscoveryYear', 'fldName'], ascending=[False, True, True]).to_csv(f, index=False)
    
    f = pd.read_csv('./data/field_percentage_produced.csv').sort_values(by=['percentageProducedOil', 'fldDiscoveryYear', 'fldName'], ascending=[False, True, True])
    f = f[f.percentageProducedOil >= 0]
    f.to_csv('./data/field_percentage_produced_oil.csv', index=False)
    
    f = pd.read_csv('./data/field_percentage_produced.csv').sort_values(by=['percentageProducedGas', 'fldDiscoveryYear', 'fldName'], ascending=[False, True, True])
    f = f[f.percentageProducedGas >= 0]
    f.to_csv('./data/field_percentage_produced_gas.csv', index=False)