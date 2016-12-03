#!/bin/bash

set -ex

unamestr=`uname`

docker_ip="127.0.0.1"
self_ip="127.0.0.1"

if [[ "$unamestr" == "Darwin" ]]; then
  echo "setting up for OS X..."
  docker-machine --version
  docker-machine status default
  docker-machine start default &>/dev/null || true
  docker_ip="$(docker-machine ip default)"
  echo "docker ip is $docker_ip"
  self_ip="10.0.2.2"
  echo "setting up for OS X... OK"
fi

docker stop manet &>/dev/null || true
docker rm manet &>/dev/null || true

docker run -d --net=host --name=manet -p=8891:8891 pdelsante/manet

./node_modules/.bin/webpack-dev-server ./vis/entry --hot --inline --module-bind "css=style\!css" &
SERVER_PID=$!
sleep 5 # such hack...

echo "starting to take screenshots"

curl -H "Content-Type: application/json" -d '{"url":"'$self_ip':8080/bundle?mode=oil", "force": true, "width": 10, "height": 10}' http://$docker_ip:8891/ > ./img/oil_production_yearly_12MMA_by_discovery_decade.png
curl -H "Content-Type: application/json" -d '{"url":"'$self_ip':8080/bundle?mode=gas", "force": true, "width": 10, "height": 10}' http://$docker_ip:8891/ > ./img/gas_production_yearly_12MMA_by_discovery_decade.png
curl -H "Content-Type: application/json" -d '{"url":"'$self_ip':8080/bundle?mode=petroleum", "force": true, "width": 10, "height": 10}' http://$docker_ip:8891/ > ./img/oe_production_yearly_12MMA_by_discovery_decade.png

curl -H "Content-Type: application/json" -d '{"url":"'$self_ip':8080/bundle?mode=oil_region", "force": true, "width": 10, "height": 10}' http://$docker_ip:8891/ > ./img/oil_production_yearly_12MMA_by_region.png
curl -H "Content-Type: application/json" -d '{"url":"'$self_ip':8080/bundle?mode=gas_region", "force": true, "width": 10, "height": 10}' http://$docker_ip:8891/ > ./img/gas_production_yearly_12MMA_by_region.png
curl -H "Content-Type: application/json" -d '{"url":"'$self_ip':8080/bundle?mode=petroleum_region", "force": true, "width": 10, "height": 10}' http://$docker_ip:8891/ > ./img/oe_production_yearly_12MMA_by_region.png

docker stop manet
docker rm manet
kill $SERVER_PID
