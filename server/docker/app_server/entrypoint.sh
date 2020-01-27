#!/bin/sh

cd app_server
gunicorn -w 4 --bind 0.0.0.0:8000 --worker-class aiohttp.GunicornWebWorker\
    "server:app_factory('cfg/cfg.yml')"
