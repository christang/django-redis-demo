#!/usr/bin/env bash

pip install -r requirements.txt

./manage.py syncdb
./manage.py migrate
