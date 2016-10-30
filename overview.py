#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import datetime
import locale

import pandas as pd


def get_contribution(filename, decade):
    frame = pd.read_csv(filename)
    frame = frame.tail(1)
    p = 100.0*frame[decade] / frame['Sum']
    return "%.1f" % (p.values[0])

def show_relative_contribution():
    print("""\n## Prosent av nåværende produksjon

Tabellen under angir prosentvis bidrag til petroleumsproduksjon på norsk sokkel. 
Disse er gruppert på funntiår.
Man kan med andre ord se at funn gjort på 1970-tallet noenlunde dominerer produksjonen. 
\n""")
    frame = pd.read_csv('./data/oe_production_by_discovery_decade.csv')
    frame = frame.tail(1)
    decades = frame.columns
    decades = decades[decades.str.isnumeric()].values
    print("| Funntiår | Olje | Gass | Petroleum |")
    print("| ---- | ---: | ---: | ---: |")
    for dec in decades:
        v = []
        v.append(get_contribution('./data/oil_production_by_discovery_decade.csv', dec))
        v.append(get_contribution('./data/gas_production_by_discovery_decade.csv', dec))
        v.append(get_contribution('./data/oe_production_by_discovery_decade.csv', dec))
        print("|", dec, "|", " | ".join(v), "|")

if __name__=="__main__":
    locale.setlocale(locale.LC_TIME, 'no_NO')

    def short_summary(prefix, filename, unit):
        frame = pd.read_csv(filename)
        last = frame.tail(1)['Sum'].values[0]
        mx = frame['Sum'].max()
        print("")
        def format_date(v):
            return datetime.date(int(v.split("-")[0]), int(v.split("-")[1]), 1).strftime('%B %Y')
        print(prefix, "per %s er på" % (format_date(frame.tail(1)['Date'].values[0])), 
                "%.2f %s," % (last, unit), 
                "som er", "%.1f%%" % (100.0 * (last / mx)),
                "av nivået i %s" % (format_date(frame[frame['Sum'] == mx]['Date'].values[0])),
                "(%.2f %s)." % (mx, unit)
                )
    print("# Oversikt over norsk sokkel\n")
    short_summary('Oljeproduksjonen', './data/oil_production_monthly_12MMA_mboe_d_by_discovery_decade.csv', 'Million fat/dag')
    short_summary('Gassproduksjonen', './data/gas_production_monthly_12MMA_mboe_d_by_discovery_decade.csv', 'Million fat oljeekvivalenter/dag')
    short_summary('Petroleumproduksjonen', './data/oe_production_monthly_12MMA_mboe_d_by_discovery_decade.csv', 'Million fat oljeekvivalenter/dag')

    print("")

    show_relative_contribution()
