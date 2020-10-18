## Imagem base
FROM python:3.7.9-alpine3.12

## Atualiza pacotes do Alpine
RUN apk update

## Instala dependências do psycopg2
RUN apk add postgresql-dev gcc python3-dev musl-dev

## Instala dependências do pyzmq
RUN apk add build-base libzmq musl-dev python3 python3-dev zeromq-dev

## Cria diretório raiz
RUN mkdir -p /backend

## Copia arquivos para o diretório raiz
COPY . /backend

## Define o diretório raiz
WORKDIR /backend

## Instala dependências
RUN pip install -r requirements.txt

## Inicia o publisher de cotações (DEV!)
CMD watchmedo auto-restart -p "*.py" -R python -- publisher/publisher.py