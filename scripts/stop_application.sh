#!/usr/bin/env bash
cd /home/ubuntu/www/backend/
source /home/ubuntu/www/backend/venv/bin/activate
# supervisorctl -c /home/ubuntu/www/backend/supervisor/default.conf stop all 2&>1 >/dev/null
# sudo unlink /tmp/supervisor.sock 2> /dev/null
sudo pkill supervisor*
