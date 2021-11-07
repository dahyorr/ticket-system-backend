FROM python:3.9.7-alpine
LABEL author='dahyor'

WORKDIR /code
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
EXPOSE 8000

COPY requirements.txt .
RUN apk add --update --no-cache --virtual .tmp-build-deps \
	gcc musl-dev libffi-dev
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN apk del .tmp-build-deps

COPY . .

RUN adduser -D user
USER user
