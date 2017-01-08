#!/usr/bin/env python3

import datetime
import locale
import textwrap

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
        print("Dette gjev ein årleg produksjon på", ("%.1f" % ((last*365.0)/1000.0)).replace('.', ','), "milliardar fat.")
            
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
    print(add_norwegian_comma_and_dot("Dei opphavlege utvinnbare %s er på %.1f milliardar %s" % (reserve_name, originally_in_place, unit)))
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

def oversikt_etter_produksjonsstartår(remainingField='remainingOil', remainingField2='fldRemainingOil', prefixFilename='oil', resource='olje', unit='olje'):
    frame = pd.read_csv('./data/region/reserves_gboe_by_startproduction.csv')
    reserves = pd.read_csv('./data/raw_reserves_field.csv')
    før_2000_reserves_gb = frame[frame['name'] == 'Før 2000'][remainingField].values[0]
    før_2000_produsert_gb = frame[frame['name'] == 'Før 2000']['origRecoverable' + (remainingField.replace('remaining', ''))].values[0] - før_2000_reserves_gb
    etter_2000_reserves_gb = frame[frame['name'] == 'Etter 2000'][remainingField].values[0]
    sverdrup_reserver_db = reserves[reserves['fldName'] == 'JOHAN SVERDRUP'][remainingField2].values[0] * (6.29/1000.0)
    
    last_production = pd.read_csv('./data/millennium/' + prefixFilename + '_production_yearly_12MMA_mboe_d_by_startproduction.csv').tail(1)
    før_2000_prosent_produksjon = 100.0*last_production['Før 2000'] / last_production['Sum']

    return(textwrap.dedent("""
    ![Produksjon](img/oil_production_yearly_12MMA_by_startproduction.png)
    Felt med produksjonsstart før år 2000 står for {}% av dagens {}produksjon.

    ![Produsert og reserver](img/oil_produced_reserves_by_startproduction.png)

    Reservane for felt med produksjonsstart før år 2000 er på {} milliardar fat %UNIT%, og
    totalt har desse felta produsert {} milliardar fat %UNIT%.

    Reservane for felt med produksjonsstart etter år 2000 er på {} milliardar fat %UNIT%.
    Johan Sverdrup (med planlagt produksjonsstart i 2019) har {}% av desse ({} milliardar fat %UNIT%).
    """.format(
        ("%.0f" % (før_2000_prosent_produksjon.values[0])).replace(".", ","),
        resource,
        str(før_2000_reserves_gb).replace(".", ","),
        str(før_2000_produsert_gb).replace(".", ","),
        str(etter_2000_reserves_gb).replace(".", ","),
        ("%.0f" % ((100.0*sverdrup_reserver_db) / etter_2000_reserves_gb)).replace(".", ","),
        ("%.1f" % (sverdrup_reserver_db)).replace(".", ",")
    )).strip().replace('oil', prefixFilename).replace('%UNIT%', unit)
    )


def oversikt_etter_region(remainingField='remainingOil', prefixFilename='oil', resource='olje', unit='olje'):
    last_production = pd.read_csv('./data/region/' + prefixFilename + '_production_yearly_12MMA_mboe_d_by_region.csv').tail(1)
    regions = ['North sea']

    def reserves(region):
        frame = pd.read_csv('./data/region/reserves_gboe_by_region.csv')
        sm = frame[frame['name'] == 'Sum'][remainingField].values[0]
        region_value = frame[frame['name'] == region][remainingField].values[0]
        return ("%.f%% (%.1f milliardar fat %s)" % (region_value*100 / sm, region_value, unit)).replace('.', ',')
    print(textwrap.dedent("""
    ![Produksjon](img/oil_production_yearly_12MMA_by_region.png)
    Nordsjøen står for %North sea%% av %resource%produksjonen,
    Norskehavet %Norwegian sea%% og
    Barentshavet %Barents sea%%.

    ![Produsert og reserver](img/oil_produced_reserves_by_region.png)
    Nordsjøen har %North sea reserves% av %resource%reservane.

    Norskehavet har %Norwegian sea reserves% av %resource%reservane.
    
    Barentshavet har %Barents sea reserves% av %resource%reservane.
    """)
    .replace('oil', prefixFilename)
    .replace('%resource%', resource)
    .replace('%North sea%', "%.0f" % (last_production['North sea']*100.0 / last_production['Sum']).values[0])
    .replace('%Norwegian sea%', "%.0f" % (last_production['Norwegian sea']*100.0 / last_production['Sum']).values[0])
    .replace('%Barents sea%', "%.0f" % (last_production['Barents sea']*100.0 / last_production['Sum']).values[0])
    .replace('%North sea reserves%', reserves('North sea'))
    .replace('%Norwegian sea reserves%', reserves('Norwegian sea'))
    .replace('%Barents sea reserves%', reserves('Barents sea'))
    )

if __name__=="__main__":
    try:
        locale.setlocale(locale.LC_TIME, 'nb_NO.UTF-8') # needed for month formatting (august, juni, etc.)
    except:
        locale.setlocale(locale.LC_TIME, 'no_NO') # needed for month formatting (august, juni, etc.)

        
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
    print("# Oversikt over norsk sokkel etter produksjonsstartår\n")
    print("## Olje")
    print(oversikt_etter_produksjonsstartår())

    print("\n## Gass")
    print(oversikt_etter_produksjonsstartår(remainingField='remainingGas', remainingField2='fldRemainingGas', prefixFilename='gas', resource='gass', unit='oljeekvivalentar'))

    print("\n## Petroleum")
    print(oversikt_etter_produksjonsstartår(remainingField='remainingOE', remainingField2='fldRemainingOE', prefixFilename='oe', resource='petroleum', unit='oljeekvivalentar'))
    
    print("")
    print("# Oversikt over norsk sokkel etter region\n")
    print("## Olje")
    oversikt_etter_region()
    print("\n## Gass")
    oversikt_etter_region(prefixFilename='gas', resource='gass', remainingField='remainingGas', unit='oljeekvivalentar')
    print("\n## Petroleum")
    oversikt_etter_region(prefixFilename='oe', resource='petroleum', remainingField='remainingOE', unit='oljeekvivalentar')
