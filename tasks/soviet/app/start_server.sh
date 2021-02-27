#!/usr/bin/env bash

rm -f $1/soviet.sock
exec socat -T30 unix-l:$1/soviet.sock,fork exec:"$(pwd)/worker.py $1"
