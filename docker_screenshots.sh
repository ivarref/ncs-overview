#!/bin/bash

set -ex

docker stop manet || echo "ignore"
docker rm manet || echo "ignore"

CONTAINER=$(docker run -d --net=host --name=manet -p=8891:8891 pdelsante/manet)

echo $CONTAINER

./node_modules/.bin/webpack-dev-server ./vis/entry --hot --inline --module-bind "css=style\!css" &
SERVER_PID=$!
sleep 5 # such hack...

echo "starting to take screenshots"

curl -H "Content-Type: application/json" -d '{"url":"localhost:8080/bundle?mode=oil&", "force": true, "width": 10, "height": 10}' http://localhost:8891/ > ./img/oil_production_yearly_12MMA_by_discovery_decade.png
curl -H "Content-Type: application/json" -d '{"url":"localhost:8080/bundle?mode=gas", "force": true, "width": 10, "height": 10}' http://localhost:8891/ > ./img/gas_production_yearly_12MMA_by_discovery_decade.png
curl -H "Content-Type: application/json" -d '{"url":"localhost:8080/bundle?mode=petroleum", "force": true, "width": 10, "height": 10}' http://localhost:8891/ > ./img/oe_production_yearly_12MMA_by_discovery_decade.png

curl -H "Content-Type: application/json" -d '{"url":"localhost:8080/bundle?mode=oil_region", "force": true, "width": 10, "height": 10}' http://localhost:8891/ > ./img/oil_production_yearly_12MMA_by_region.png
curl -H "Content-Type: application/json" -d '{"url":"localhost:8080/bundle?mode=gas_region", "force": true, "width": 10, "height": 10}' http://localhost:8891/ > ./img/gas_production_yearly_12MMA_by_region.png
curl -H "Content-Type: application/json" -d '{"url":"localhost:8080/bundle?mode=petroleum_region", "force": true, "width": 10, "height": 10}' http://localhost:8891/ > ./img/oe_production_yearly_12MMA_by_region.png

docker stop manet
docker rm manet
kill $SERVER_PID
