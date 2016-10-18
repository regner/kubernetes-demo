


FROM python:3.5.2-alpine
MAINTAINER Regner Blok-Andersen <shadowdf@gmail.com>

ADD requirements.txt main.py /app/

WORKDIR /app/

RUN pip install -qU pip \
  && pip install -r requirements.txt

CMD gunicorn main:app -w 1 -b 0.0.0.0:8000 --log-level info --timeout 120 --pid /app/main.pid
