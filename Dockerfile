FROM python:3.12-alpine

WORKDIR /home/app

COPY . .

RUN apk update && \
    apk upgrade && \
    apk add python3 && \
    apk add py3-pip && \
    apk add postgresql && \
    apk add postgresql-contrib && \
    apk add postgresql-libs && \
    apk add geos && \
    apk add gdal && \
    apk add gdal-dev && \
    apk add geos-dev && \
    apk add proj && \
    apk add proj-dev && \
    apk add postgis && \
    apk add supervisor && \
    apk add celery && \
    apk add nginx

COPY ./nginx/nginx.conf /etc/nginx/nginx.conf
#COPY supervisor/conf.d /etc/supervisor/conf.d
RUN adduser -D -H azadi

ENV GDAL_LIBRARY_PATH=/usr/lib/libgdal.so
ENV GEOS_LIBRARY_PATH=/usr/lib/libgeos_c.so
RUN pip install --upgrade pip
RUN pip install -r /home/app/requirements.txt
RUN python /home/app/manage.py collectstatic --settings=shop.settings.production
RUN chown -R azadi:azadi /home/app/static
RUN chmod +x /home/app/start.sh
ENV PYTHONDDONOTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

#EXPOSE 8000
ENTRYPOINT [ "gunicorn", "shop.wsgi", "-b"]
CMD ["0.0.0.0:8000"]
