# Slightly modified from
# https://www.caktusgroup.com/blog/2017/03/14/production-ready-dockerfile-your-python-django-app/
#FROM python:3.6-alpine
FROM python:3.6
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

# I'm not sure what these are for tbh but yeah
RUN apt-get update && apt-get install -y curl \
    build-essential \
    libpq-dev

ADD requirements.txt .
RUN pip install -U -r requirements.txt

ADD . .

EXPOSE 5000

ENTRYPOINT ["./entrypoint.sh"]