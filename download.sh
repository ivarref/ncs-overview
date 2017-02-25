#!/bin/bash

set -ex

# factpages.npd.no -> Discovery -> Table view -> Overview -> Export CSV
curl "http://factpages.npd.no/ReportServer?/FactPages/TableView/discovery&rs:Command=Render&rc:Toolbar=false&rc:Parameters=f&rs:Format=CSV&Top100=false&IpAddress=80.213.255.240&CultureCode=en" \
| tr -d '\r' \
| grep -vi "^31/6-1 TROLL ØST,Statoil Petroleum AS,PRODUCING,OIL/GAS,31/6-1,North sea,TROLL,15.12.1986,1983,,BUSINESS ARRANGEMENT AREA,TROLL UNIT,44552,46437" \
| grep -vi "INCLUDED IN OTHER DISCOVERY" \
| awk 'NR==1{sub(/^\xef\xbb\xbf/,"")}{print}' \
| awk 'NF' > data/raw_discovery_overview.csv
head -n1 data/raw_discovery_overview.csv > ./data/ignore_discovery.csv
#diff <(head -n 1 data/raw_discovery_overview.csv) <(./extra_data/generate_discovery_overview_extra_csv.py | head -n 1)
#./extra_data/generate_discovery_overview_extra_csv.py | tail -n +2 >> data/raw_discovery_overview.csv
./drop_columns.py ./data/raw_discovery_overview.csv dscDateUpdated dscDateUpdatedMax DatesyncNPD
./explode_csv.py ./data/raw_discovery_overview.csv ./data/raw_discovery_overview.json


curl "http://factpages.npd.no/ReportServer?/FactPages/TableView/discovery&rs:Command=Render&rc:Toolbar=false&rc:Parameters=f&rs:Format=CSV&Top100=false&IpAddress=80.213.255.240&CultureCode=en" \
| tr -d '\r' \
| grep -vi "^31/6-1 TROLL ØST,Statoil Petroleum AS,PRODUCING,OIL/GAS,31/6-1,North sea,TROLL,15.12.1986,1983,,BUSINESS ARRANGEMENT AREA,TROLL UNIT,44552,46437" \
| grep -i "INCLUDED IN OTHER DISCOVERY" \
| awk 'NR==1{sub(/^\xef\xbb\xbf/,"")}{print}' \
| awk 'NF' >> data/ignore_discovery.csv
./drop_columns.py ./data/ignore_discovery.csv dscDateUpdated dscDateUpdatedMax DatesyncNPD
./explode_csv.py ./data/ignore_discovery.csv ./data/ignore_discovery.json

curl "http://factpages.npd.no/ReportServer?/FactPages/TableView/field_production_monthly&rs:Command=Render&rc:Toolbar=false&rc:Parameters=f&rs:Format=CSV&Top100=false&IpAddress=80.213.255.240&CultureCode=en" \
| tr -d '\r' \
| grep -vi "^33/9-6 DELTA" \
| awk 'NR==1{sub(/^\xef\xbb\xbf/,"")}{print}' \
| awk 'NF' > data/raw_production_monthly_field.csv

mkdir -p tmp_data/

curl "http://factpages.npd.no/ReportServer?/FactPages/TableView/field_reserves&rs:Command=Render&rc:Toolbar=false&rc:Parameters=f&rs:Format=CSV&Top100=false&IpAddress=80.213.255.240&CultureCode=en" \
| tr -d '\r' \
| awk 'NR==1{sub(/^\xef\xbb\xbf/,"")}{print}' \
| awk 'NF' > data/raw_reserves_field.csv
./drop_columns.py data/raw_reserves_field.csv DatesyncNPD fldDateOffResEstDisplay
./add_discovery_year.py
./drop_columns.py data/raw_reserves_field_discovery_year_mboe.csv fldRecoverableNGL fldRecoverableCondensate fldRemainingNGL fldRemainingCondensate
cp -fv ./data/raw_reserves_field_discovery_year.csv ./data/raw_reserves_field.csv

cp -fv data/raw_reserves_field.csv data/raw_reserves_field_original_recoverable.csv
./drop_columns.py data/raw_reserves_field_original_recoverable.csv fldRecoverableNGL fldRecoverableCondensate fldRemainingOil fldRemainingGas fldRemainingNGL fldRemainingCondensate fldRemainingOE
./explode_csv.py data/raw_reserves_field_original_recoverable.csv data/raw_reserves_field_original_recoverable.json

# factpages.npd.no -> Field -> Table view -> Production -> Saleable -> Yearly - total
curl "http://factpages.npd.no/ReportServer?/FactPages/TableView/field_production_totalt_NCS_year__DisplayAllRows&rs:Command=Render&rc:Toolbar=false&rc:Parameters=f&rs:Format=CSV&Top100=false&IpAddress=80.213.255.240&CultureCode=en" \
| tr -d '\r' \
| awk 'NR==1{sub(/^\xef\xbb\xbf/,"")}{print}' \
| awk 'NF' > data/raw_production_yearly_total.csv

# factpages.npd.no -> Discovery -> Table view -> Resources -> Export CSV
curl "http://factpages.npd.no/ReportServer?/FactPages/TableView/discovery_reserves&rs:Command=Render&rc:Toolbar=false&rc:Parameters=f&rs:Format=CSV&Top100=false&IpAddress=80.213.255.240&CultureCode=en" \
| tr -d '\r' \
| awk 'NR==1{sub(/^\xef\xbb\xbf/,"")}{print}' \
| sed 's/^ //g' \
| awk 'NF' > data/raw_discovery_resources.csv
./drop_columns.py data/raw_discovery_resources.csv dscDateOffResEstDisplay dscReservesDateUpdated DatesyncNPD
./add_discovery_year2.py > ./tmp.csv
mv -fv tmp.csv data/raw_discovery_resources.csv
./explode_csv.py data/raw_discovery_resources.csv data/raw_discovery_resources.json

# factpages.npd.no -> Field -> Table view -> Production -> Saleable -> Yearly - by field
curl "http://factpages.npd.no/ReportServer?/FactPages/TableView/field_production_yearly&rs:Command=Render&rc:Toolbar=false&rc:Parameters=f&rs:Format=CSV&Top100=false&IpAddress=129.177.92.109&CultureCode=en" \
| tr -d '\r' \
| awk 'NR==1{sub(/^\xef\xbb\xbf/,"")}{print}' \
| sed '/33\/9-6 DELTA/d' \
| awk 'NF' > data/raw_production_yearly_field.csv

echo "download.sh OK"