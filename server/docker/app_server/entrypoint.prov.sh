#!/bin/sh

cd app_server
python3 provision.py --db-host='social-mysql' --db-port=3306 --db-user='root' --db-password=''
