#!/bin/bash

echo "Waiting for PostgreSQL to start..."
while ! nc -z postgres_db 5432; do
  sleep 0.1
done
echo "PostgreSQL is up!"

python manage.py migrate
python manage.py runserver 0.0.0.0:8000 