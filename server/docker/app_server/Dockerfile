FROM ubuntu:18.04

RUN apt-get update
RUN apt-get -y install python3 python3-pip
RUN pip3 install PyMySQL gunicorn asyncio aiohttp pyjwt aiomysql
RUN pip3 install requests pyyaml
RUN pip3 install russian-names

COPY server/docker/app_server/entrypoint.sh /entrypoint.sh
COPY server/docker/app_server/entrypoint.prov.sh /entrypoint.prov.sh
COPY server/app /app_server/

ENTRYPOINT ["/entrypoint.sh"]
