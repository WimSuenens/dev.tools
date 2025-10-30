#!/bin/bash

# Start Nginx
nginx

# Apply database migrations
python3 /app/server/manage.py migrate --noinput

# Start Gunicorn
cd /app/server

# https://pythonspeed.com/articles/gunicorn-in-docker/
gunicorn --worker-tmp-dir /dev/shm  --workers 2 --threads=4 --worker-class=gthread application.wsgi:application --bind 0.0.0.0:8000