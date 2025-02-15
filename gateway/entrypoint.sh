#!/bin/bash
set -e

# Czekaj na dostępność bazy danych
echo "Waiting for database..."
until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER"
do
    echo "Database is unavailable - sleeping"
    sleep 1
done
echo "Database started"

# Czekaj na dostępność Redis
echo "Waiting for Redis..."
python << END
import sys
import redis
import time
import os

redis_url = os.environ.get('REDIS_URL')

while True:
    try:
        redis_client = redis.from_url(redis_url)
        redis_client.ping()
        break
    except redis.ConnectionError:
        print("Redis is unavailable - sleeping")
        time.sleep(1)
print("Redis started")
END

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
