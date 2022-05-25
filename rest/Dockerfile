FROM python:3.6-slim
LABEL MAINTAINER="Maaz Shaikh <maaz.shaikh@colorado.edu>"

RUN pip3 install --upgrade flask pyopenssl cryptography pika redis jsonpickle requests psycopg2-binary
RUN pip3 install pyjwt==1.7.1  
ENV PYTHONUNBUFFERED=0

WORKDIR /srv
COPY . /srv/

CMD ["python3", "-u", "rest-server.py", "|& tee /proc/1/fd/1"]