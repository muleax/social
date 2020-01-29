FROM nginx:1.16.1

RUN apt-get update
RUN apt-get -y install nano net-tools

COPY server/docker/nginx_proxy/entrypoint.sh /entrypoint.sh
COPY server/nginx_proxy /nginx_proxy/
COPY client /app_client/

CMD nginx -c /nginx_proxy/nginx.conf
