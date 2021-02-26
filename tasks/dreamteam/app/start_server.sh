#!/usr/bin/env bash
set -e

mkdir -p $1

TYPE=dreamteam exec ./server.py $1

