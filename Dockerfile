FROM python:3.12-alpine

WORKDIR /home/app

COPY . .
COPY ./start.sh .

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
    apk add supervisor

RUN adduser --disabled-password azadi
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN chmod +x /home/app/start.sh
RUN python manage.py collectstatic --noinput
ENV PYTHONDDONOTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV GDAL_LIBRARY_PATH=/usr/lib/libgdal.so
ENV PROJ_LIB=/usr/share/proj

ENV DJANGO_SUPERUSER_PASSWORD=Admin.1234

EXPOSE 8000

ENTRYPOINT [ "gunicorn", "--bind", "0.0.0.0:8000", "shop.wsgi:application" ]
CMD [ "/home/app/start.sh" ]
