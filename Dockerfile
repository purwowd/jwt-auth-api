FROM python:3.7-alpine
LABEL maintainer="id.purwowd@gmail.com"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN apk update
RUN apk --update add \
    build-base \
    jpeg-dev \
    zlib-dev
RUN apk add --no-cache postgresql-client
RUN apk add --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers musl-dev \
    zlib zlib-dev jpeg-dev postgresql-dev
RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps

RUN mkdir /src
WORKDIR /src
COPY ./src /src

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static
RUN adduser -D user
RUN chown -R user:user /vol/
RUN chmod -R 755 /vol/web
USER user
