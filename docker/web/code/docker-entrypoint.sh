#!/bin/bash


#pip install -r requirements.txt
#pip install pur
#pip install --upgrade -r requirements.txt

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput

# ждем пока БД загрузится
sleep 20
# Apply database migrations
echo "Apply database migrations"
python manage.py migrate


#ping -n 3 db
# Start server
echo "Starting server"
python manage.py runserver 0.0.0.0:8000