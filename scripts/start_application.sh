#!/usr/bin/env bash

cd /home/ubuntu/www/backend/
source /home/ubuntu/www/backend/venv/bin/activate
echo yes | /home/ubuntu/www/backend/manage.py collectstatic
supervisord -c /home/ubuntu/www/backend/supervisor/default.conf