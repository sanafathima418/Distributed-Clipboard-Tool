FROM python:3.6-slim
LABEL MAINTAINER="Maaz Shaikh <maaz.shaikh@colorado.edu>"

RUN  pip3 install pika

WORKDIR /srv
COPY    logs.py /srv
CMD [ "python3", "logs.py"]
