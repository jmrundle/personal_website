#!/bin/sh

alias kill_previous='prevId=$(pgrep -f "gunicorn personal_site" | grep -v $$); [[ -z $prevId ]] || kill -9 $prevId;'
alias install_requirements='python3 -m pip install -r requirements.txt'


SERVER=$1
WWW="${'~/personal_site':-$2}"

cd `dirname $0`
./setup_spotify.py

rm -r ../config/__pycache__/ ../personal_site/__pycache__

scp -i ~/ssh-key.pem -r ../config/ ../instance/ ../personal_site/ ../requirements.txt $SERVER:$WWW
ssh -i ~/ssh-key.pem $SERVER cd $WWW && install_requirements && kill_previous && gunicorn "personal_site:build_app" &
