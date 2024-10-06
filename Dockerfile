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
    apk add postgis && \
    apk add supervisor && \
    apk add celery && \
    apk add nginx

COPY ./nginx/nginx.conf /etc/nginx/nginx.conf
COPY supervisor/conf.d /etc/supervisor/conf.d
RUN adduser -D -H azadi
RUN pip install --upgrade pip
RUN pip install -r /home/app/requirements/production.txt
RUN /home/app/manage.py collectstatic --noinput
RUN chmod +x /home/app/start.sh
ENV PYTHONDDONOTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

#EXPOSE 8000
ENTRYPOINT [ "gunicorn", "shop.wsgi", "-b"]
CMD ["/home/app/start.sh"]
