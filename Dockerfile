FROM python:3.7.8-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

RUN apk add --update --no-cache jpeg-dev

RUN apk add --update --no-cache --virtual .tmp-build-deps \
  gcc libc-dev linux-headers musl-dev zlib zlib-dev

RUN mkdir /code
WORKDIR /code

COPY Pipfile* ./

RUN pip3 install --upgrade pip && \
  pip3 install --no-cache-dir pipenv

RUN pipenv install --system --dev

RUN apk del .tmp-build-deps

COPY . .

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static

RUN adduser -D worker

RUN chown -R worker:worker /vol/
RUN chmod -R 755 /vol/web

USER worker
