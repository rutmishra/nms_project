#!/bin/sh

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to start..."
/wait-for-it.sh postgres_db:5432 --timeout=30 --strict -- echo "PostgreSQL is up!"

# Run database migrations
echo "Running migrations..."
python manage.py migrate

# Start Django server
echo "Starting Django server..."
exec python manage.py runserver 0.0.0.0:8000
