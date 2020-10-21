# Desafio PontoTel
## Ibovespa/Empresas

Esse projeto é um desafio da PontoTel em seu proceso de seleção de devs.
O desafio foi desenvolver um sistema para fornecer informações de cotação em tempo real do Ibovespa e das 10 maiores empresas brasileiras.

- Um preview do sistema desenvolvido pode ser acessado aqui: https://davidborges.xyz/desafio-pontotel
- A documentação da API pode ser acessada aqui: https://davidborges.xyz/ibovespa-empresas-backend/docs

## Backend

- Implementei o backend usando [FastAPI](https://fastapi.tiangolo.com/) como framework web e [SQLAlchemy](https://www.sqlalchemy.org/) para interação com o banco de dados [PostreSQL](https://www.postgresql.org/).
- Para realizar as requisições à API do [Alpha Vantage](https://www.alphavantage.co/), implementei um módulo contendo classes e funções para facilitar as operações.
- Devido às limitações da API, com permissão de apenas 5 requests por minuto, implementei algumas medidas extras.
A primeira foi o uso de um cache baseado em [Redis](https://redis.io/) para armazenar algumas requests e reduzir chamadas à API para requisições recentes.
A segunda foi o uso de múltiplas chaves de API e roteamento via [Tor](https://www.torproject.org/) para estender o limite de chamadas ao Alpha Vantage.
- Implementei com [pytest](https://docs.pytest.org/en/latest/) cerca de 30 testes de sanidade para as funções da API de backend e do módulo de interação com o Alpha Vantage.
- Também implementei um módulo para facilitar a comunicação com o banco de dados.
- As migrações iniciais do BD foram realizadas com [Alembic](https://alembic.sqlalchemy.org/en/latest/).
- Desenvolvi um publisher de cotações que trabalha em um processo separado do backend principal, com a função de coletar dados de cotação 
para as 10 empresas cadastradas de 3 em 3 minutos a partir da API do Alpha Vantage e armazená-los no BD. Simultaneamente, esses dados são
enviados ao backend principal via [ZeroMQ](https://zeromq.org/) usando o padrão de comunicação PUB/SUB. O backend principal é responsável por enviar esses 
dados ao frontend, em tempo real, via websocket, quando solicitado.
- Para organizar e facilitar o desenvolvimento, utilizei [Docker](https://www.docker.com/) e [Docker Compose](https://docs.docker.com/compose/) para criar os 5 containers que participam das operações do backend. São eles: Postgres, Redis, Proxy TOR, o backend principal e o publisher de cotações.

#### Executar o backend (modo desenvolvedor)
A partir do diretório /backend
```
docker-compose up
```
CTRL-C para interromper o processo

#### Realizar as migrações iniciais (popular o BD com 10 empresas)
Em outro terminal, a partir do diretório /backend
```
docker exec -it bovespa-empresas-backend alembic upgrade head
```

#### Executar os testes (necessário ter o backend em execução)
Em outro terminal, a partir do diretório /backend
```
docker exec -it bovespa-empresas-backend python -m pytest
```

#### Resetar o estado do BD, Redis, etc
```
docker-compose down
```

## Frontend

- Implementei o front usando Vue.js e aproveitei alguns componentes desenvolvidos pela comunidade, por exemplo: [vue-chartjs](https://vue-chartjs.org/) para gráficos e [vue-sidebar-menu](https://github.com/yaminncco/vue-sidebar-menu) para o menu lateral.
- O código do front foi dividido em múltiplos componentes para possibilitar o reuso de funcionalidades.
- As informações em tempo real são atualizadas através de comunicação via websocket com o backend, que submete atualizações de cotação tão logo essas são recebidas a partir do publisher.
- Vuex é usado para guardar informações úteis ao front e reduzir a necessidade de novas requisições. As empresas cadastradas, por exemplo, já são armazenadas.

#### Instalar dependências
A partir do diretório /frontend
```
npm install
```

#### Iniciar o frontend (modo desenvolvedor)
```
npm run serve
```

## Problemas enfrentados

- Atualmente, a API do Alpha Vantage não atualiza os valores de cotação em tempo real. Percebi isso depois de um tempo, quando notei que todos os valores enviados pela API eram iguais e que só sofriam alteração ao final do dia. A função GLOBAL_QUOTE, por exemplo, que deveria ser em tempo real, demora bastante a ser atualizada. A função TIME_SERIES_INTRADAY também apresenta o mesmo problema.
- Diversos símbolos que há alguns meses funcionavam na API do Alpha Vantage deixaram de funcionar. Por exemplo, li que o símbolo "^BVSP" era utilizado para obter cotações do Ibovespa, no entanto, atualmente o uso desse símbolo retorna erro. Para obter os valores do Ibovespa, tive que selecionar um outro símbolo de um patrimônio (BOVB11.SAO) que espelha o Ibovespa e, portanto, deve seguir a mesma cotação.
- A API do Alpha Vantage não disponibiliza a função TIME_SERIES_INTRADAY para as 10 maiores empresas do Brasil. O retorno para essas empresas brasileiras geralmente é um erro. Essa mesma função, quando utilizada com um outro símbolo, por exemplo "IBM", retorna como esperado (infelizmente, ainda com valores desatualizados).

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
