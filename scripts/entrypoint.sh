#!/bin/bash

# Start Nginx
nginx

# Apply database migrations
python3 /app/server/manage.py migrate --noinput

# Start Gunicorn
cd /app/server
gunicorn application.wsgi:application --bind 0.0.0.0:8000 --workers 3