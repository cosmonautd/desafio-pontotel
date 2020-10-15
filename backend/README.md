## Inicialização

#### Passo 1: Iniciar usando Docker Compose

```docker-compose up```

#### Passo 2: Executar migrações
```docker exec -it bovespa-empresas-backend alembic upgrade head```