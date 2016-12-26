#!/bin/bash

curl "http://factpages.npd.no/ReportServer?/FactPages/TableView/wellbore_exploration_all&rs:Command=Render&rc:Toolbar=false&rc:Parameters=f&rs:Format=CSV&Top100=false&IpAddress=37.253.210.126&CultureCode=en" \
| tr -d '\r' \
| awk 'NR==1{sub(/^\xef\xbb\xbf/,"")}{print}' \
| sed 's/NORTH SEA/North sea/g' \
| sed 's/NORWEGIAN SEA/Norwegian sea/g' \
| sed 's/BARENTS SEA/Barents sea/g' \
| awk 'NF' > data/raw_wellbore.csv

./drop_columns.py data/raw_wellbore.csv wlbDateUpdated wlbDateUpdatedMax datesyncNPD

./explode_csv.py data/raw_wellbore.csv data/raw_wellbore.json
