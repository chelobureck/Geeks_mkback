#!/bin/bash

echo "Building project..."
# Install dependencies
python3.12 -m pip install -r requirements.txt

# Collect static files
echo "Collecting static files..."
python3.12 manage.py collectstatic --noinput

echo "Build finished."
