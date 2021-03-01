#!/usr/bin/env bash

set -e

npm install

mkdir -p $1

exec ./server.js $1
