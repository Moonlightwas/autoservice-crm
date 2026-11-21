#!/bin/sh
set -e

python manage.py migrate
python manage.py collectstatic
cp -r /app/static/. /backend_static/

python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();

User.objects.filter(email='admin@example.com').exists() or User.objects.create_superuser(
    email='admin@example.com', password='qwerty@123', role='admin');

User.objects.filter(email='mechanic@example.com').exists() or User.objects.create_user(
    email='mechanic@example.com', password='qwerty@123', role='mechanic');
    
User.objects.filter(email='client@example.com').exists() or User.objects.create_user(
    email='client@example.com', password='qwerty@123', role='client')
"

exec "$@" 