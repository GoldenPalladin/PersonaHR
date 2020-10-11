#!/usr/bin/env bash
chown ubuntu:ubuntu /home/ubuntu/www
virtualenv /home/ubuntu/www/backend/venv
chown ubuntu:ubuntu /home/ubuntu/www/backend/venv
chown ubuntu:ubuntu /home/ubuntu/www/backend/venv/*
source /home/ubuntu/www/backend/env/bin/activate
pip install -r /home/ubuntu/www/backend/requirements.txt