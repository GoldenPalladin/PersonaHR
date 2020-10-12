#!/usr/bin/env bash
cd /home/ubuntu/www/backend/
cp db.sqlite3 /tmp
source /home/ubuntu/www/backend/venv/bin/activate
sudo service apache2 stop
