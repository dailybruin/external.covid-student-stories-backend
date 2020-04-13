#!/bin/sh
set -e

# reason for this is because migration 0003 seems to be breaking for some reason on the rancher container
# python covidstudents/manage.py migrate
# python covidstudents/manage.py migrate student_stories 0003_auto_20200411_1914 --fake

python covidstudents/manage.py migrate
gunicorn --bind 0.0.0.0:8000 --pythonpath covidstudents covidstudents.wsgi:application --daemon

exec "$@"
