FROM python:3.7.8-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

RUN mkdir /code
WORKDIR /code

COPY Pipfile* /code/

RUN apk add --update --no-cache postgresql-client jpeg-dev && \
  apk add --update --no-cache --virtual .tmp-build-deps \
  gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev

RUN pip install --upgrade pip && \
  pip install pipenv && \
  pipenv lock && \
  pipenv install --dev --system

RUN apk del .tmp-build-deps

COPY . /code/

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static

RUN adduser -D worker

RUN chown -R worker:worker /vol/
RUN chmod -R 755 /vol/web

USER worker
