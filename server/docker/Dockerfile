FROM ubuntu:18.04

RUN apt-get update
RUN apt-get -y install python3 python3-pip
RUN pip3 install PyMySQL

COPY docker/entrypoint.sh /entrypoint.sh
COPY src /server/

ENTRYPOINT ["/entrypoint.sh"]