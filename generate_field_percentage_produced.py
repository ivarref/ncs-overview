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
        else:
          newrow = []
          writer.writerow([value('fldName'), value('fldDiscoveryYear'), percentage('Oil'), percentage('Gas'), percentage('OE')])
        pass

    