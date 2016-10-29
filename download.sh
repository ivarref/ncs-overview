#!/bin/bash

curl "http://factpages.npd.no/ReportServer?/FactPages/TableView/field_reserves&rs:Command=Render&rc:Toolbar=false&rc:Parameters=f&rs:Format=CSV&Top100=false&IpAddress=84.208.153.159&CultureCode=en" \
| awk 'NR==1{sub(/^\xef\xbb\xbf/,"")}{print}' > raw_reserves.csv

curl "http://factpages.npd.no/ReportServer?/FactPages/TableView/discovery&rs:Command=Render&rc:Toolbar=false&rc:Parameters=f&rs:Format=CSV&Top100=false&IpAddress=80.213.255.240&CultureCode=en" \
| awk 'NR==1{sub(/^\xef\xbb\xbf/,"")}{print}' > raw_discovery_overview.csv

curl "http://factpages.npd.no/ReportServer?/FactPages/TableView/field_production_monthly&rs:Command=Render&rc:Toolbar=false&rc:Parameters=f&rs:Format=CSV&Top100=false&IpAddress=80.213.255.240&CultureCode=en" \
| awk 'NR==1{sub(/^\xef\xbb\xbf/,"")}{print}' > raw_production_monthly_field.csv

head -n10 raw_production_monthly_field.csv > snip_raw_production_monthly_field.csv
