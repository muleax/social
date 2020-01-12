FROM nginx:1.17.7

COPY docker/nginx_proxy/entrypoint.sh /entrypoint.sh
COPY nginx_proxy /nginx_proxy/

ENTRYPOINT ["/entrypoint.sh"]
