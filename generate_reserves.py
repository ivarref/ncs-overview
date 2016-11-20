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
  
  def sum_entry(decade, fields, mod_fn=lambda prop, v: v):
    def sum_prop(destination_prop, prop):
        return (destination_prop, mod_fn(destination_prop, sum([remaining_reserve(field_id, prop) for field_id in fields])))
    d = collections.OrderedDict([
        ('name', str(decade)),
        sum_prop('origRecoverableOil', 'fldRecoverableOil'),
        sum_prop('origRecoverableGas', 'fldRecoverableGas'),
        sum_prop('origRecoverableOE', 'fldRecoverableOE'),
        sum_prop('remainingOil', 'fldRemainingOil'),
        sum_prop('remainingGas', 'fldRemainingGas'),
        sum_prop('remainingOE', 'fldRemainingOE')])
    return d
  
  with codecs.open('./data/reserves_OEMillSm3_by_decade.csv', mode='w', encoding='utf8') as wfd:
    def write(line):
      wfd.write(line)
      wfd.write("\n")
      print(line)
    decades = decade_to_fields.items()
    decades.append(('Sum', ids))
    for (idx, (decade, fields)) in enumerate(decades):
      d = sum_entry(decade, fields)
      if (idx == 0):
        write(",".join(d.keys()))
      write(",".join([str(x) for x in d.values()]))
  print("-"*80)

  with codecs.open('./data/reserves_percentage_by_decade.csv', mode='w', encoding='utf8') as wfd:
    def write(line):
      wfd.write(line)
      wfd.write("\n")
      print(line)
    decades = decade_to_fields.items()
    decades.append(('Sum', ids))
    o = sum_entry('Sum', ids)
    for (idx, (decade, fields)) in enumerate(decades):
      def relative(prop, v):
        return "%.2f" % ((100.0*v) / o[prop])
      d = sum_entry(decade, fields, relative)
      if (idx == 0):
        write(",".join(d.keys()))
      write(",".join([str(x) for x in d.values()]))
  print("-"*80)
