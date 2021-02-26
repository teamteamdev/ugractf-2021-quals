#!/usr/bin/env bash
set -e

mkdir -p $1

TYPE=smallercitylights ./server.py $1

