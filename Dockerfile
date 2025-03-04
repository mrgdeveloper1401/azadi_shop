FROM python:3.12-alpine3.20

WORKDIR /home/app

COPY . .

RUN apk update && \
    apk upgrade && \
    apk add python3 && \
    apk add py3-pip && \
    apk add postgresql && \
    apk add celery && \
    apk add nginx

RUN adduser -D -H azadi

RUN pip install --upgrade pip
RUN pip install -r /home/app/requirements/production.txt
RUN python /home/app/manage.py collectstatic --settings=shop.settings.production

ENV PYTHONDDONOTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

#EXPOSE 8000
ENTRYPOINT [ "gunicorn", "shop.wsgi", "-b"]
CMD ["0.0.0.0:8000"]
