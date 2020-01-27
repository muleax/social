#!/usr/bin/env bash

# TODO: add m/s build
docker build -t nginx-proxy -f server/docker/nginx_proxy/Dockerfile .
docker build -t app-server -f server/docker/app_server/Dockerfile .
docker build -t social-mysql -f server/docker/mysql/Dockerfile .
