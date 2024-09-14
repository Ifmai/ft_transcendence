#!/bin/sh

until pg_isready -h ${USER_DB_HOST} -U ${USER_DB_USER} -p ${USER_DB_PORT}; do
  >&2 echo "Veritabanı Api42 hazır değil - bekleniyor..."
  sleep 2
done

>&2 echo "Veritabanı hazır."

python manage.py makemigrations
python manage.py migrate

exec "$@"