#!/usr/bin/env bash

cd /home/ubuntu/www/backend/
mkdir /static
source /home/ubuntu/www/backend/venv/bin/activate
echo yes | /home/ubuntu/www/backend/manage.py collectstatic
sudo service apache2 start