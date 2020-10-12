#!/usr/bin/env bash
cp /tmp/db.sqlite3 /home/ubuntu/www/backend/sqlite3
cd /home/ubuntu/www/backend/
source /home/ubuntu/www/backend/venv/bin/activate
python ./manage.py makemigrations
python ./manage.py migrate