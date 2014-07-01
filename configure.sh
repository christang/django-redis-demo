#!/usr/bin/env bash

###################
#  Run me first!  #
###################

pip install -r requirements.txt && \
./manage.py syncdb && \
./manage.py migrate && \
./manage.py collectstatic && \
clear

echo
tput bold
echo This project will utilize the DATABASE_URL environment variable
echo to configure its database connection, and REDIS_CONN to configure
echo its Redis cache.
tput sgr0
echo 
echo Typically, the DATABASE_URL will look like:
echo \"postgres://user:pass@localhost:5432/db\"
echo
echo Yours is set to:
tput setaf 2
echo \"$DATABASE_URL\"
tput sgr0
echo
echo The REDIS_CONN will look like:
echo \"localhost:6379:1\"
echo
echo Yours is set to:
tput setaf 2
echo \"$REDIS_CONN\"
tput sgr0
echo
