#!/usr/bin/env bash

trap 'kill $(jobs -p)' EXIT
nginx -p $PWD/nginx -c nginx.conf &
./text_server.py &
dropbear -r dropbear.key -F -b banner.txt -s -p 127.0.0.1:1722 -E -j -k -c false &
sudo sslh -Fsslh.cfg
