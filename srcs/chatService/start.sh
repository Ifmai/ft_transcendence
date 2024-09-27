#!/bin/sh

until pg_isready -h ${USER_DB_HOST} -U ${USER_DB_USER} -p ${USER_DB_PORT}; do
  >&2 echo "Veritabanı Api42 hazır değil - bekleniyor..."
  sleep 2
done

>&2 echo "Veritabanı hazır."

X=17

while true; do
  TABLE_COUNT=$(PGPASSWORD="$USER_DB_PASS" psql -h "$USER_DB_HOST" -U "$USER_DB_USER" -p "$USER_DB_PORT" -d "$USER_DB_NAME" -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';" | xargs)

  if [ "$TABLE_COUNT" -ge "$X" ]; then
    echo "Koşul sağlandı. Toplam tablo sayısı: $TABLE_COUNT"
    break
  else
    echo "Koşul sağlanmadı. Tablo sayısı: $TABLE_COUNT - Bekleniyor..."
  fi

  sleep 5
done

python manage.py makemigrations
python manage.py migrate --fake

exec "$@"
