FROM nginx:1.17.7

COPY server/docker/nginx_proxy/entrypoint.sh /entrypoint.sh
COPY server/nginx_proxy /nginx_proxy/
COPY client /app_client/

CMD nginx -c /nginx_proxy/nginx.conf
