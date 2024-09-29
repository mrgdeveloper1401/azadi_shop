FROM python:3.12-alpine

WORKDIR /home/app

COPY . .

RUN apk update && \
    apk upgrade && \
    apk add python3 && \
    apk add py3-pip && \
    apk add postgresql-client && \
    apk add gdal && \
    apk add gdal-dev && \
    apk add geos && \
    apk add geos-dev && \
    apk add build-base && \
    apk add gcc && \
    apk add musl-dev && \
    apk add postgresql-dev && \
    apk add libffi-dev && \
    apk add libpq-dev && \
    apk add libxslt-dev && \
    apk add jpeg-dev && \
    apk add libxml2-dev && \
    apk add linux-headers && \
    apk add libjpeg && \
    apk add zlib-dev && \
    apk add libxml2 && \
    apk add supervisor && \
    apk add nginx

COPY ./nginx/nginx.conf /etc/nginx/nginx.conf
RUN adduser --disabled-password azadi
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ENV PYTHONDDONOTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV GDAL_LIBRARY_PATH=/usr/lib/libgdal.so
ENV PROJ_LIB=/usr/share/proj

EXPOSE 80

ENTRYPOINT [ "gunicorn", "shop.wsgi", "-b"]
CMD ["0.0.0.0:8000"]
