#!/bin/bash
set -e

# Zastosuj migracje
echo "Applying database migrations..."
python manage.py migrate

# Uruchom Celery w tle
echo "Starting Celery worker..."
celery -A core worker --loglevel=info &

# Uruchom pierwszy task przetwarzania telemetrii
echo "Starting telemetry processing..."
python manage.py shell -c "from devices.tasks import process_telemetry_queue; process_telemetry_queue.delay()"

# Uruchom serwer Django
echo "Starting Django server..."
python manage.py runserver 0.0.0.0:8000
