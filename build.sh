#!/usr/bin/env bash

docker build -t nginx-proxy -f server/docker/nginx_proxy/Dockerfile .
docker build -t app-server -f server/docker/app_server/Dockerfile .
