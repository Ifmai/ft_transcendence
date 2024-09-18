#!/bin/sh

until pg_isready -h users_db -U authuser -p 5432; do
  >&2 echo "Veritabanı Api42 hazır değil - bekleniyor..."
  sleep 2
done


>&2 echo "Veritabanı hazır."

python manage.py makemigrations
python manage.py migrate

exec "$@"
