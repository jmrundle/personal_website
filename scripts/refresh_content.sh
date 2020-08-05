#!/bin/sh

# refreshes website content (deletes all on remote, then copies local to remote)
#   - must be ran from project root (TODO: change this)


if [ $# -lt 2 ]; then
    echo "Usage $0 SERVER WWW";
    exit;
fi


SERVER=$1
WWW=$2
ALL=0


if [ $# -eq 3 ]; then
    ALL=$3;
fi


echo "Cleaning up local repo"
rm -rf config/__pycache__/ personal_site/__pycache__
rm -f config/.DS_Store personal_site/.DS_Store


echo "Cleaning up remote repo"
if [ $ALL -eq 1 ]; then
    ssh -i ~/ssh-key.pem $SERVER "mkdir -p $WWW && cd $WWW && rm -rf config/ instance/ personal_site/ requirements.txt"
else
    ssh -i ~/ssh-key.pem $SERVER "mkdir -p $WWW && cd $WWW && rm -rf instance/"
fi

echo "Copying source files to remote"
if [ $ALL -eq 1 ]; then
    scp -q -i ~/ssh-key.pem -r config instance personal_site requirements.txt $SERVER:$WWW
else
    scp -q -i ~/ssh-key.pem -r instance $SERVER:$WWW
fi
