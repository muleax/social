#!/bin/sh

cd app_server
gunicorn -w 4 --bind 0.0.0.0:8000 --worker-class aiohttp.GunicornWebWorker\
    "server:app_factory('social-mysql', 3306, 'root', '')"
