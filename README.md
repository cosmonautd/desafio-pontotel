# Desafio PontoTel
## Ibovespa/Empresas

Esse projeto é um desafio da PontoTel em seu proceso de seleção de devs.
O desafio foi desenvolver um sistema para fornecer informações de cotação em tempo real do Ibovespa e das 10 maiores empresas brasileiras.

## Backend

- Implementei o backend usando FastAPI como framework web e SQLAlchemy para interação com o banco de dados PostreSQL.
- Para realizar as requisições à API do Alpha Vantage, implementei um módulo contendo classes e funções para facilitar as operações.
- Devido às limitações da API, com permissão de apenas 5 requests por minuto, implementei algumas medidas extras.
A primeira foi o uso de um cache baseado em Redis para armazenar algumas requests e reduzir chamadas à API para requisições recentes.
A segunda foi o uso de múltiplas chaves de API e roteamento via TOR para estender o limite de chamadas ao Alpha Vantage.
- Implementei com Pytest cerca de 30 testes de sanidade para as funções da API de backend e do módulo de interação com o Alpha Vantage.
- Também implementei um módulo para facilitar a comunicação com o banco de dados.
- As migrações iniciais do BD foram realizadas com Alembic.
- Desenvolvi um publisher de cotações que trabalha em um processo separado do backend principal, com a função de coletar dados de cotação 
para as 10 empresas cadastradas de 3 em 3 minutos a partir da API do Alpha Vantage e armazená-los no BD. Simultaneamente, esses dados são
enviados ao backend principal via ZeroMQ usando o padrão de comunicação PUB/SUB. O backend principal é responsável por enviar esses 
dados ao frontend, em tempo real, via websocket, quando solicitado.
- Para organizar e facilitar o desenvolvimento, utilizei Docker e Docker Compose para criar os 5 containers que participam das operações
do backend. São eles: Postgres, Redis, Proxy TOR, o backend principal e o publisher de cotações.

#### Executar o backend
```
docker-compose up
```

#### Realizar as migrações iniciais (popular o BD com as 10 empresas iniciais)
```
docker exec -it bovespa-empresas-backend alembic upgrade head
```

#### Executar os testes (necessário ter o backend em execução)
```
docker exec -it bovespa-empresas-backend python -m pytest
```

#### Resetar o estado do BD, Redis, etc
```
docker-compose down
```

## Frontend

...

## Passos do desafio

### Level 1

- [x] Escrever um programa que consulte o número de pontos do bovespa usando o alpha vantage (registro simples para obter chave de api aqui: https://www.alphavantage.co/support/#api-key)
- [x] Validar o input da API para garantir que ela sempre esteja correta
- [x] Apresentar esse número em uma página html
- [x] Deixar usuário informar qual empresa (listar 10 maiores brasileiras) ele quer ver o preço do momento
- [x] Escrever testes

### Level 2

- [x] Modelar Usuário, Empresa e Cotação em um banco de dados relacional (Postgres)
- [ ] Escrever as opções do usuário em um banco de dados postgres

### Level 3

- [x] Apresentar esse número em tempo real usando um framework async de python

### Level 4

- [x] Utilizar o Zeromq para criar um pipeline de trabalho que mostra o valor atual e a derivada das empresas selecionadas

### Level 5

- [x] Plotar em tempo real a evolução das cotações no front, suas derivadas (do level 4)

### BÔNUS

### Level 6 (Front)

- [x] implementar leitura dinamica dos valores em framework React ou VueJs

### Level 7 (Front)

- [ ] Uso de css-grid e variáveis para tornar design responsivo
- [x] Guardar estado da aplicação em Vuex ou Redux

### Level 8 (Front)

- [ ] User um service worker para estimar dinamicamente tendência (reta) das cotações coletadas até agora.
- [ ] Apresentar essa reta na tela


### Pontos extras para:

- [x] Documentação da API (swagger, etc)
- [x] Testes (+1 com Pytest)
- [ ] Async
- [x] Validação dos inputs
- [x] Tipagem
