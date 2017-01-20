#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import codecs
import collections
import csv
import json
import sys

import pandas as pd

import generate


def get_distinct_fields():
  frame = pd.read_csv('./data/raw_reserves_field.csv')
  ids = frame[u'fldName'].unique()
  return sorted(ids)

def remaining_reserve(field_id, kind):
  frame = pd.read_csv('./data/raw_reserves_field.csv')
  f = frame[frame[u'fldName'] == field_id]
  return f[kind].values[0]

if __name__=="__main__":
  # get distinct field ids
  ids = get_distinct_fields()

  # group fields by discovery decade
  decade_to_fields = generate.get_decade_to_fields(generate.get_discovery_years(ids))
  region_to_fields = generate.get_discovery_region_to_fields(ids)
  millennium_to_fields = generate.get_production_years(get_distinct_fields())

  with open('./data/region_to_fields_reserves.json', 'w') as wfd:
    json.dump(region_to_fields, wfd, sort_keys=True, indent=2, ensure_ascii=False)
  
  with open('./data/decade_to_fields_reserves.json', 'w') as wfd:
    json.dump(decade_to_fields, wfd, sort_keys=True, indent=2, ensure_ascii=False)

  with open('./data/startproduction_to_fields_reserves.json', 'w') as wfd:
    json.dump(millennium_to_fields, wfd, sort_keys=False, indent=2, ensure_ascii=False)


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

  def write_file(group_to_ids, filname, mod_fn=lambda prop, v: v):
    with codecs.open(filname, mode='w', encoding='utf8') as wfd:
      for (idx, (group, fields)) in enumerate(group_to_ids):
        d = sum_entry(group, fields, mod_fn)
        if (idx == 0):
          write(wfd, ",".join(d.keys()))
        write(wfd, ",".join([str(x) for x in d.values()]))
    print("-"*80)

  decades = []
  decades.extend(decade_to_fields.items())
  decades.append(('Sum', ids))

  regions = []
  regions.extend(region_to_fields.items())
  regions.append(('Sum', ids))

  millenniums = []
  millenniums.extend(millennium_to_fields.items())
  millenniums.append(('Sum', ids))

  write_file(decades, './data/decade/reserves_OEMillSm3_by_decade.csv')
  write_file(regions, './data/region/reserves_OEMillSm3_by_region.csv')
  write_file(millenniums, './data/region/reserves_OEMillSm3_by_startproduction.csv')

  o = sum_entry('Sum', ids)
  def relative(prop, v):
    return "%.2f" % ((100.0*v) / o[prop])
  write_file(decades, './data/decade/reserves_percentage_by_decade.csv', relative)
  write_file(regions, './data/region/reserves_percentage_by_region.csv', relative)
  write_file(millenniums, './data/region/reserves_percentage_by_startproduction.csv', relative)

  def gboe(prop, v):
    return "%.1f" % ((v*6.29) / 1000.0)
  write_file(decades, './data/decade/reserves_gboe_by_decade.csv', gboe)
  write_file(regions, './data/region/reserves_gboe_by_region.csv', gboe)
  write_file(millenniums, './data/region/reserves_gboe_by_startproduction.csv', gboe)

  oil_giants = generate.get_giant_status(get_distinct_fields(), 'fldRecoverableOil')
  gas_giants = generate.get_giant_status(get_distinct_fields(), 'fldRecoverableGas')
  oe_giants = generate.get_giant_status(get_distinct_fields(), 'fldRecoverableOE')
  
  frame = pd.read_csv('./data/raw_reserves_field.csv')
  # name,origRecoverableOil,origRecoverableGas,origRecoverableOE,remainingOil,remainingGas,remainingOE

  gigant = []
  ikkje_gigant = []
  def produce_row(kind):
    fldNames = oil_giants[kind]
    origRecoverableOil = gboe('', frame[frame.fldName.isin(fldNames)].fldRecoverableOil.sum())
    origRecoverableGas = gboe('', frame[frame.fldName.isin(fldNames)].fldRecoverableGas.sum())
    origRecoverableOE = gboe('', frame[frame.fldName.isin(fldNames)].fldRecoverableOE.sum())
    remainingOil = gboe('', frame[frame.fldName.isin(fldNames)].fldRemainingOil.sum())
    remainingGas = gboe('', frame[frame.fldName.isin(fldNames)].fldRemainingGas.sum())
    remainingOE = gboe('', frame[frame.fldName.isin(fldNames)].fldRemainingOE.sum())

    return [kind, origRecoverableOil, origRecoverableGas, origRecoverableOE, remainingOil, remainingGas, remainingOE]
  with open('./data/giants/reserves_gboe_by_fieldsize.csv', 'w') as wfd:
    writer = csv.writer(wfd)
    writer.writerow('name,origRecoverableOil,origRecoverableGas,origRecoverableOE,remainingOil,remainingGas,remainingOE'.split(","))
    writer.writerow(produce_row('Gigant'))
    writer.writerow(produce_row('Ikkje gigant'))
