#!/bin/sh

if [ "$POSTGRES_DB" = "store" ]
then
    echo "Wait postgres..."

    while ! nc -z "db" $POSTGRES_PORT; do
      sleep 0.5
    done

    echo "PostgreSQL is ready!"
fi

python manage.py makemigrations
python manage.py migrate
python manage.py loaddata fixtures/all_data.json

exec "$@"