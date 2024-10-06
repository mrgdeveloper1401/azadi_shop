FROM python:3.12-alpine

WORKDIR /home/app

COPY . .

RUN apk update && \
    apk upgrade && \
    apk add python3 && \
    apk add py3-pip && \
    apk add postgresql && \
    apk add postgresql-contrib && \
    apk add postgis && \
    apk add supervisor && \
    apk add nginx

COPY ./nginx/nginx.conf /etc/nginx/nginx.conf
RUN adduser --disabled-password azadi
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN ./manage.py collectstatic --noinput
ENV PYTHONDDONOTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

#EXPOSE 8000
ENTRYPOINT [ "gunicorn", "shop.wsgi", "-b"]
CMD ["0.0.0.0:8000"]
