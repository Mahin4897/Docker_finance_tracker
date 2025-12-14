#!/bin/sh
set -e

echo "Waiting for MySQL..."

while ! mysqladmin ping -h"$DB_HOST" -u"$DB_USER" -p"$DB_PASSWORD" --silent; do
  sleep 1
done

echo "MySQL is up!"

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput

exec gunicorn finance_tracker.wsgi:application --bind 0.0.0.0:8000
