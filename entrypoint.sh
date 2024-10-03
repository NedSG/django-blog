#!/bin/bash

echo "Create migrations"
python manage.py makemigrations --noinput

echo "Apply database migrations"
python manage.py migrate

echo "Preload database data"
python manage.py loaddata --format=json db_data

echo "Collect static files"
python manage.py collectstatic --noinput

exec "$@"