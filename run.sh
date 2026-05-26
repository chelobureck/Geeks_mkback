#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Apply database migrations
echo "Applying database migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
# Clear static directory to avoid stale files
rm -rf /app/static/*
python manage.py collectstatic --noinput --clear

# Start Gunicorn
echo "Starting server..."
exec gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 120
