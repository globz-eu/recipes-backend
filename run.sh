#!/bin/bash

set -e

pip3 install --no-cache-dir -r requirements.txt
pip3 install uwsgi
python manage.py collectstatic --noinput
python ./manage.py makemigrations
python ./manage.py migrate
uwsgi --ini ./uwsgi.ini
