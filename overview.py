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
    return ("%.1f" % (p.values[0])).replace('.', ',')

def show_relative_contribution():
    print("""\n## Prosent av nåværende produksjon

Tabellen under angir prosentvis bidrag til petroleumsproduksjon på norsk sokkel. 
Disse er gruppert på funntiår.
Man kan med andre ord se at funn gjort på 1970-tallet noenlunde dominerer produksjonen. 
\n""")
    frame = pd.read_csv('./data/decade/oe_production_yearly_12MMA_MillSm3_by_discovery_decade.csv')
    frame = frame.tail(1)
    decades = frame.columns
    decades = decades[decades.str.isnumeric()].values
    print("| Funntiår | Olje | Gass | Petroleum |")
    print("| ---- | ---: | ---: | ---: |")
    for dec in decades:
        v = []
        v.append(get_contribution('./data/decade/oil_production_yearly_12MMA_MillSm3_by_discovery_decade.csv', dec))
        v.append(get_contribution('./data/decade/gas_production_yearly_12MMA_BillSm3_by_discovery_decade.csv', dec))
        v.append(get_contribution('./data/decade/oe_production_yearly_12MMA_MillSm3_by_discovery_decade.csv', dec))
        print("|", dec, "|", " | ".join(v), "|")

if __name__=="__main__":
    try:
        locale.setlocale(locale.LC_TIME, 'nb_NO.UTF-8') # needed for month formatting (august, juni, etc.)
    except:
        locale.setlocale(locale.LC_TIME, 'no_NO') # needed for month formatting (august, juni, etc.)

    def short_summary(title, prefix, filename, unit, image, image_produced_reserves, include_text_description=True):
        frame = pd.read_csv(filename)
        last = frame.tail(1)['Sum'].values[0]
        mx = frame['Sum'].max()
        print("## " + title)
        print("![%s](%s)" % (prefix, image))
        print("")

        def format_date(v):
            return datetime.date(int(v.split("-")[0]), int(v.split("-")[1]), 1).strftime('%B %Y')
        
        if include_text_description:
            print(prefix, "per %s er på" % (format_date(frame.tail(1)['Date'].values[0])), 
                    "%s %s," % (("%.2f" % (last)).replace('.', ','), unit), 
                    "som er", 
                    ("%.1f%%" % (100.0 * (last / mx))).replace('.', ','),
                    "av nivået i %s" % (format_date(frame[frame['Sum'] == mx]['Date'].values[0])),
                    ("(%.2f %s)" % (mx, unit)).replace('.', ',')+'.'
                    )
        print("")
        print("![Produsert og reserver](%s)" % (image_produced_reserves))
        print("")

    def add_norwegian_comma_and_dot(s):
        return s.replace(".", ",") + '.'

    def percentage_produced(resource_key, reserve_name, unit):
        frame = pd.read_csv('./data/decade/reserves_gboe_by_decade.csv')
        frame = frame[frame['name'] == 'Sum']
        (originally_in_place, remaining) = (frame.tail(1)["origRecoverable" + resource_key].values[0], frame.tail(1)["remaining" + resource_key].values[0])
        produced = originally_in_place - remaining
        produced_percentage = (produced*100.0) / originally_in_place
        print(add_norwegian_comma_and_dot("Dei opprinnelig utvinnbare %s er på %.1f milliardar %s" % (reserve_name, originally_in_place, unit)))
        print(add_norwegian_comma_and_dot("Totalt %.1f%% av desse er utvunne" % (produced_percentage)))
        print(add_norwegian_comma_and_dot("Gjenverande reservar er på %.1f milliardar %s" % (remaining, unit)))

        try:
            frame = pd.read_csv('./data/decade/%s_production_yearly_12MMA_MillSm3_by_discovery_decade.csv' % (resource_key.lower()))
        except:
            frame = pd.read_csv('./data/decade/%s_production_yearly_12MMA_BillSm3_by_discovery_decade.csv' % (resource_key.lower()))
        current_production_millSm3 = frame.tail(1)['Sum'].values[0]
        current_production_gboe = (current_production_millSm3*6.29) / 1000.0
        num_years = remaining / current_production_gboe
        print(add_norwegian_comma_and_dot("Med noverande produksjonstempo er desse reservane utvunne på %.1f år" % (num_years)))
        print("")
        
    print("# Oversikt over norsk sokkel etter funntiår\n")
    short_summary('Olje', 'Oljeproduksjonen', './data/decade/oil_production_monthly_12MMA_mboe_d_by_discovery_decade.csv', 'millionar fat/dag', 'img/oil_production_yearly_12MMA_by_discovery_decade.png', 'img/oil_produced_reserves_by_discovery_decade.png')
    percentage_produced('Oil', "oljereservane", "fat")

    short_summary('Gass', 'Gassproduksjonen', './data/decade/gas_production_monthly_12MMA_mboe_d_by_discovery_decade.csv', 'millionar fat oljeekvivalentar/dag', 'img/gas_production_yearly_12MMA_by_discovery_decade.png', 'img/gas_produced_reserves_by_discovery_decade.png')
    percentage_produced('Gas', "gassreservane", "fat oljeekvivalent")

    short_summary('Petroleum', 'Petroleumproduksjonen', './data/decade/oe_production_monthly_12MMA_mboe_d_by_discovery_decade.csv', 'millionar fat oljeekvivalentar/dag', 'img/oe_production_yearly_12MMA_by_discovery_decade.png', 'img/oe_produced_reserves_by_discovery_decade.png')
    percentage_produced('OE', "petroleumreservane", "fat oljeekvivalent")

    print("")

    show_relative_contribution()

    print("")
    print("# Oversikt over norsk sokkel etter region\n")

    short_summary('Olje', 'Oljeproduksjonen', './data/region/oil_production_monthly_12MMA_mboe_d_by_region.csv', 'millionar fat/dag', 'img/oil_production_yearly_12MMA_by_region.png', 'img/oil_produced_reserves_by_region.png', False)
    short_summary('Gass', 'Gassproduksjonen', './data/region/gas_production_monthly_12MMA_mboe_d_by_region.csv', 'millionar fat oljeekvivalentar/dag', 'img/gas_production_yearly_12MMA_by_region.png', 'img/gas_produced_reserves_by_region.png', False)
    short_summary('Petroleum', 'Petroleumproduksjonen', './data/region/oe_production_monthly_12MMA_mboe_d_by_region.csv', 'millionar fat oljeekvivalentar/dag', 'img/oe_production_yearly_12MMA_by_region.png', 'img/oe_produced_reserves_by_region.png', False)
