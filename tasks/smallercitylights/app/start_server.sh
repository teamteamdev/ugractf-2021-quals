#!/usr/bin/env bash
set -e

mkdir -p $1

TYPE=smallercitylights exec ./server.py $1

