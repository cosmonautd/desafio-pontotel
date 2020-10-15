## Imagem base
FROM python:3.7.9-alpine3.12

## Atualiza pacotes do Alpine
RUN apk update

## Instala dependências do psycopg2
RUN apk add postgresql-dev gcc python3-dev musl-dev

## Cria diretório raiz
RUN mkdir -p /backend

## Copia arquivos para o diretório raiz
COPY . /backend

## Define o diretório raiz
WORKDIR /backend

## Instala dependências
RUN pip install -r requirements.txt

## Inicia a API (DEV!)
CMD uvicorn main:app --reload --host 0.0.0.0 --port 8000