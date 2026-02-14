#!/bin/sh

echo "Aguardando Postgres..."
while ! nc -z postgres_db 5432; do
  sleep 1
done

echo "Postgres disponível, aplicando migrations..."
python manage.py migrate

echo "Iniciando servidor ASGI..."
exec "$@"
