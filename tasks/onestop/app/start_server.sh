#!/bin/sh

trap 'kill $(jobs -p)' EXIT
./https_server.py &
./text_server.py &
dropbear -r dropbear.key -F -b banner.txt -s -p 1722 -E -j -k -c false &
sslh -F sslh.cfg
