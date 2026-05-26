#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Create migrations for apps
echo "Creating migrations..."
python manage.py makemigrations users
python manage.py makemigrations education

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start Gunicorn
echo "Starting server..."
exec gunicorn core.wsgi:application --bind 0.0.0.0:8000
