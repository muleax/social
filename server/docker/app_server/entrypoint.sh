#!/bin/sh

gunicorn -w 4 --bind 0.0.0.0:8000 app_server.server:app
