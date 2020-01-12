FROM ubuntu:18.04

RUN apt-get update
RUN apt-get -y install python3 python3-pip
RUN pip3 install PyMySQL gunicorn asyncio aiohttp

COPY docker/app_server/entrypoint.sh /entrypoint.sh
COPY docker/app_server/entrypoint.prov.sh /entrypoint.prov.sh
COPY src /app_server/

ENTRYPOINT ["/entrypoint.sh"]
