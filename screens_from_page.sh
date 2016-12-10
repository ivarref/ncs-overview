#!/bin/bash

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
  eval "$(docker-machine env --shell bash default)"
  echo "setting up for OS X... OK"
fi

docker stop manet &>/dev/null || true
docker rm manet &>/dev/null || true

docker run -d --net=host --name=manet -p=8891:8891 pdelsante/manet

./node_modules/.bin/webpack-dev-server $1 --hot --inline --module-bind "css=style\!css" &
SERVER_PID=$!
sleep 5 # such hack...

echo "starting to take screenshots ..."

self_ip="$self_ip" docker_ip="$docker_ip" ./screens_from_page.py $1

docker stop manet
docker rm manet
kill $SERVER_PID

