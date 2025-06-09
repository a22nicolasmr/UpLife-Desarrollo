#!/bin/sh

# while ! nc -z $DB_HOST $DB_PORT; do sleep 1; done

python manage.py makemigrations --noinput
python manage.py migrate --noinput

# echo "📦 Cargando datos (si backup existe)..."
# if [ -f "backup.json" ]; then
#   python manage.py loaddata backup.json
# fi

python manage.py collectstatic --noinput

exec gunicorn UpLife.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 3
