#!/bin/sh
set -e

# FUTURE SELF: MAKE MANUAL MIGRATIONS THE RANCHER IS RIP
# python covidstudents/manage.py makemigrations
# python covidstudents/manage.py migrate

exec "$@"