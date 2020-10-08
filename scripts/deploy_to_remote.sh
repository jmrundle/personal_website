#!/bin/sh

# deploys source files to remote machine, restarts server

if [ $# -eq 0 ]; then
    echo "Usage $0 SERVER";
    exit;
fi

SERVER=$1
WWW="~/personal_site"
SSH_PEM="~/ssh-key.pem"

# navigate to project root
cd `dirname $0`
cd ..

echo "Update spotify tokens"
export PYTHONPATH="$PYTONPATH:`pwd`"
scripts/setup_spotify.py 2> /dev/null


echo "Refreshing content"
scripts/refresh_content.sh $SERVER $WWW 1


echo "Restarting server"
ssh -f -i $SSH_PEM $SERVER "bash -s -- $WWW" < scripts/restart_server.sh
