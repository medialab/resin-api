#!/bin/bash
# Run Django migrations and collect static files

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput

# Start Gunicorn processes
echo "Starting Gunicorn."
exec gunicorn resin.wsgi:application \
    --bind 0.0.0.0:8000