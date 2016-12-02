#!/bin/bash

clear
curl -H "Content-Type: application/json" -d '{"url":"localhost:8080/bundle?mode=oil", "clipRect": "0,0,642,335", "force": true, "width": 10, "height": 10}' http://localhost:8891/ > ./img/oil_production_yearly_12MMA_by_discovery_decade.png
#./generate.py
