#!/bin/bash

python manage.py createsuperuser --noinput || echo "Superuser already exists."

python manage.py runserver 0.0.0.0:8000