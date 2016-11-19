#!/bin/bash

set -ex

mkdir -p data/

curl "http://factpages.npd.no/ReportServer?/FactPages/TableView/discovery&rs:Command=Render&rc:Toolbar=false&rc:Parameters=f&rs:Format=CSV&Top100=false&IpAddress=80.213.255.240&CultureCode=en" \
| awk 'NR==1{sub(/^\xef\xbb\xbf/,"")}{print}' > data/raw_discovery_overview.csv

curl "http://factpages.npd.no/ReportServer?/FactPages/TableView/field_production_monthly&rs:Command=Render&rc:Toolbar=false&rc:Parameters=f&rs:Format=CSV&Top100=false&IpAddress=80.213.255.240&CultureCode=en" \
| awk 'NR==1{sub(/^\xef\xbb\xbf/,"")}{print}' > data/raw_production_monthly_field.csv

curl "http://factpages.npd.no/ReportServer?/FactPages/TableView/field_reserves&rs:Command=Render&rc:Toolbar=false&rc:Parameters=f&rs:Format=CSV&Top100=false&IpAddress=80.213.255.240&CultureCode=en" \
| awk 'NR==1{sub(/^\xef\xbb\xbf/,"")}{print}' > data/raw_reserves_field.csv
