#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import pandas as pd

def get_contribution(filename, decade):
    frame = pd.read_csv(filename)
    frame = frame.tail(1)
    p = 100.0*frame[decade] / frame['Sum']
    return "%.1f" % (p.values[0])

if __name__=="__main__":
    frame = pd.read_csv('./oe_production_by_discovery_decade.csv')
    frame = frame.tail(1)
    decades = frame.columns
    decades = decades[decades.str.isnumeric()].values
    print("| Funntiår | Olje | Gass | Petroleum |")
    print("| ---- | ---: | ---: | ---: |")
    for dec in decades:
        v = []
        v.append(get_contribution('./oil_production_by_discovery_decade.csv', dec))
        v.append(get_contribution('./gas_production_by_discovery_decade.csv', dec))
        v.append(get_contribution('./oe_production_by_discovery_decade.csv', dec))
        print("|", dec, "|", " | ".join(v), "|")
