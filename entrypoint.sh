#!/bin/sh
set -e

python covidstudents/manage.py makemigrations
python covidstudents/manage.py migrate

exec "$@"