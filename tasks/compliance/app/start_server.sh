#!/usr/bin/env bash
set -ex

NEW_UUID=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)
export SOCK_PATH=$1
mkdir -p $SOCK_PATH/store
chmod 777 $SOCK_PATH/store
exec docker-compose -p "$NEW_UUID" up
