#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --noinput
python manage.py migrate --noinput

# ==== AUTO SUPERUSER (Render, no shell) ====
# Создастся только если AUTO_CREATE_SUPERUSER=1
if [ "${AUTO_CREATE_SUPERUSER}" = "1" ]; then
  export DJANGO_SUPERUSER_USERNAME="${AUTO_SUPERUSER_USERNAME:-admin}"
  export DJANGO_SUPERUSER_EMAIL="${AUTO_SUPERUSER_EMAIL:-admin@example.com}"
  export DJANGO_SUPERUSER_PASSWORD="${AUTO_SUPERUSER_PASSWORD:-admin12345}"

  # Если уже есть — команда упадет, поэтому "|| true"
  python manage.py createsuperuser --noinput || true

  echo "AUTO SUPERUSER READY: ${DJANGO_SUPERUSER_USERNAME}"
fi
