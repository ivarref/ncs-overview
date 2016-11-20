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

  # group fields by discovery decade
  decade_to_fields = generate.get_decade_to_fields(generate.get_discovery_years(ids))
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

  def write(wfd, line):
    wfd.write(line)
    wfd.write("\n")
    print(line)

  # def write_file(filname, group_to_ids, mod_fn: lambda prop, v: v):
  #   with codecs.open('./data/decade/reserves_OEMillSm3_by_decade.csv', mode='w', encoding='utf8') as wfd:

  with codecs.open('./data/decade/reserves_OEMillSm3_by_decade.csv', mode='w', encoding='utf8') as wfd:
    decades = decade_to_fields.items()
    decades.append(('Sum', ids))
    for (idx, (decade, fields)) in enumerate(decades):
      d = sum_entry(decade, fields)
      if (idx == 0):
        write(wfd, ",".join(d.keys()))
      write(wfd, ",".join([str(x) for x in d.values()]))
  print("-"*80)

  with codecs.open('./data/decade/reserves_percentage_by_decade.csv', mode='w', encoding='utf8') as wfd:
    decades = decade_to_fields.items()
    decades.append(('Sum', ids))
    o = sum_entry('Sum', ids)
    for (idx, (decade, fields)) in enumerate(decades):
      def relative(prop, v):
        return "%.2f" % ((100.0*v) / o[prop])
      d = sum_entry(decade, fields, relative)
      if (idx == 0):
        write(wfd, ",".join(d.keys()))
      write(wfd, ",".join([str(x) for x in d.values()]))
  print("-"*80)

  with codecs.open('./data/decade/reserves_gboe_by_decade.csv', mode='w', encoding='utf8') as wfd:
    decades = decade_to_fields.items()
    decades.append(('Sum', ids))
    for (idx, (decade, fields)) in enumerate(decades):
      def gboe(prop, v):
        return "%.1f" % ((v*6.29) / 1000.0)
      d = sum_entry(decade, fields, gboe)
      if (idx == 0):
        write(wfd, ",".join(d.keys()))
      write(wfd, ",".join([str(x) for x in d.values()]))
  print("-"*80)
