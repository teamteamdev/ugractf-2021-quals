#!/bin/sh
exec gunicorn -b "unix:$1/antivirus.sock" "server:make_app()"
