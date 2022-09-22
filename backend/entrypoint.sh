#!/bin/sh
python manage.py collectstatic --noinput
python manage.py migrate
python manage.py loaddata init_database.json
gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000 --timeout 90
