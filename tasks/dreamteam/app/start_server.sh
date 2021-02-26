#!/usr/bin/env bash
set -e

mkdir -p $1

TYPE=dreamteam ./server.py $1

