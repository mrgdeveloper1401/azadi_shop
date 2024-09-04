FROM python:3.12-alpine

WORKDIR /home/app

COPY . .

RUN apd update && \
    apk upgrade && \
    apk add python3-pip \
    apk add postgresql \
    apk add build-essential \
    apk add gcc \
    apk add musl-dev \
    apk add postgresql-dev \
    apk add libffi-dev \
    apk add libpq-dev

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN PYTHONDDONOTWRITEBYTECODE=1
RUN PYTHONUNBUFFERED=1

ENV DJANGO_SUPERUSER_PASSWORD=Admin.1234

EXPOSE 8000

ENTRYPOINT [ "gunicor" , "shop.wsgi", "-b"]
CMD [ "0.0.0.0:8000" ]