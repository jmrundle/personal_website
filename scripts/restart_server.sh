#!/bin/sh

# to be run on remote machine - restarts server

if [ $# -eq 0 ]; then
    echo "Usage $0 WWW";
    exit;
fi

cd $1

# Installing requirements
python3 -m pip install -r requirements.txt

# Killing previous version
killall -q gunicorn

# start server
gunicorn 'personal_site:build_app()' &
