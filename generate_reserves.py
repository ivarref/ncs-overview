#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import codecs
import collections
import sys

import pandas as pd

import generate


def get_distinct_fields():
  frame = pd.read_csv('./data/raw_reserves_field.csv')
  ids = frame[u'fldNpdidField'].unique()
  return ids

def remaining_reserve(field_id, kind):
  frame = pd.read_csv('./data/raw_reserves_field.csv')
  f = frame[frame[u'fldNpdidField'] == field_id]
  return f[kind].values[0]

if __name__=="__main__":
  # get distinct field ids
  ids = get_distinct_fields()

  # get discovery year for each id
  id_to_year = generate.get_discovery_years(ids)

  # group fields by discovery decade
  decade_to_fields = generate.get_decade_to_fields(id_to_year)
  print("reserves")
  print("-"*80)
  with codecs.open('./data/reserves_OEMillSm3_by_decade.csv', mode='w', encoding='utf8') as wfd:
    decades = decade_to_fields.items()
    decades.append(('Sum', ids))
    for (idx, (decade, fields)) in enumerate(decades):
      def write(line):
        wfd.write(line)
        wfd.write("\n")
        print(line)
      
      def sum_prop(prop):
        return sum([remaining_reserve(field_id, prop) for field_id in fields])

      d = collections.OrderedDict([
          ('name', str(decade)),
          ('origRecoverableOil', sum_prop('fldRecoverableOil')),
          ('origRecoverableGas', sum_prop('fldRecoverableGas')),
          ('origRecoverableOE', sum_prop('fldRecoverableOE')),
          ('remainingOil', sum_prop('fldRemainingOil')),
          ('remainingGas', sum_prop('fldRemainingGas')),
          ('remainingOE', sum_prop('fldRemainingOE'))])
      if (idx == 0):
        write(",".join(d.keys()))
      write(",".join([str(x) for x in d.values()]))
  print("-"*80)
