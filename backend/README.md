## Inicialização

#### Passo 1: Iniciar usando Docker Compose

```docker-compose up```

#### Passo 2: Executar migrações
```docker exec -it bovespa-empresas-backend alembic upgrade head```

#### Passo 3: Executar testes

```docker exec -it bovespa-empresas-backend python -m pytest```