#!/bin/bash

set -e

RUN='false'
COLLECT_STATIC='false'

while getopts 'r c' option; do
    case ${option} in
        'r')
            RUN='true'
            ;;
        'c')
            COLLECT_STATIC='true'
            ;;
    esac
done

if ${RUN};
then
    python manage.py makemigrations
    python manage.py migrate
    uwsgi --ini uwsgi.ini
fi
if ${COLLECT_STATIC};
then
    python manage.py collectstatic --noinput
fi
