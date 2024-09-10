FROM python:3.12-alpine

WORKDIR /home/app

COPY . .

RUN apd update && \
    apk upgrade && \
    apk add py3-pip \
    apk add postgresql-client \
    apk add build-base \
    apk add gcc \
    apk add musl-dev \
    apk add postgresql-dev \
    apk add libffi-dev \
    apk add libpq-dev \
    apk add libxslt-dev \
    apk add jpeg-dev \
    apk add libxml2-dev \
    apk add linux-headers \
    apk add libjpeg \
    apk add zlib-dev \
    apk add libxml2


RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ENV PYTHONDDONOTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENV DJANGO_SUPERUSER_PASSWORD=Admin.1234


ENTRYPOINT [ "gunicor" , "shop.wsgi", "-b"]
CMD [ "0.0.0.0:8000" ]