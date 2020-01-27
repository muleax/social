FROM mysql:8.0.18

ARG mysql_server_id

RUN mkdir -p /var/log/mysql
RUN chown -R mysql:mysql /var/log/mysql
RUN chown -R mysql:mysql /var/log/mysql

COPY server/mysql/template.cnf /etc/mysql/conf.d/template.cnf
RUN sed 's/MYSQL_SERVER_ID/'$mysql_server_id'/g' /etc/mysql/conf.d/template.cnf > /etc/mysql/conf.d/my.cnf
RUN rm /etc/mysql/conf.d/template.cnf
