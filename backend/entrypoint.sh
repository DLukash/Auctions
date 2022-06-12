#!/bin/sh

pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate

python manage.py collectstatic 

gunicorn auction_backend.wsgi:application --bind 0.0.0.0:8000
