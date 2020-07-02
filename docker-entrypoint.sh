#!/bin/bash

echo "Testing..."
pytest

echo "Apply database migrations"
python manage.py migrate

echo "Create super user"
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@myproject.com', '12345')" | python manage.py shell

echo "Start server"
python manage.py runserver 0.0.0.0:8000

