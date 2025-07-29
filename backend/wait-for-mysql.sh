#!/bin/sh

echo "Waiting for MySQL to start on port 3306..."

until nc -z -v -w30 $DB_HOST 3306
do
  echo "Waiting for database..."
  sleep 2
done

echo "Database is ready — starting app"
exec python app.py
