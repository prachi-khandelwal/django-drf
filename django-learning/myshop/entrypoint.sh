#!/bin/bash
set -e

echo "=== Starting Django Application ==="
echo "Port: ${PORT:-8000}"

echo ""
echo "Running database migrations..."
python manage.py migrate --noinput || {
    echo "ERROR: Migrations failed!"
    exit 1
}

echo ""
echo "Starting Gunicorn..."
exec gunicorn myshop.wsgi:application --bind 0.0.0.0:${PORT:-8000} --access-logfile - --error-logfile - --log-level info

