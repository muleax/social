#!/usr/bin/env bash

docker build -t nginx-proxy -f docker/nginx_proxy/Dockerfile .
docker build -t app-server -f docker/app_server/Dockerfile .
