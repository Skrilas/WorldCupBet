# WorldCupBet

Sistema de apostas desenvolvido em Python com FastAPI, baseado na Copa do Mundo de 2026.

O sistema permite que usuários criem e gerenciem apostas em partidas, acompanhem seus pontos, consultem o ranking e visualizem informações sobre partidas e seleções. Também possui uma área administrativa para gerenciamento e sincronização das partidas.

## Funcionalidades

### Usuários

* Cadastro de usuários
* Autenticação utilizando JWT
* Consulta dos dados do usuário autenticado
* Alteração de senha
* Consulta de pontos
* Consulta do ranking
* Cancelamento da participação no sistema

### Apostas

* Criação de apostas
* Consulta do status de uma aposta
* Multiplicação de apostas
* Consulta das apostas do usuário
* Consulta das apostas ativas
* Distribuição de pontos após o resultado das partidas

### Partidas

* Consulta de partidas
* Consulta de uma partida específica

### Times

* Consulta de times
* Consulta do histórico de participações dos times nas Copas do Mundo anteriores

### Administração

* Listagem de usuários
* Busca de usuário por CPF
* Sincronização das partidas
* Consulta dos times de uma partida
* Liberação de partidas para apostas
* Consulta geral das apostas de uma partida


## Tecnologias utilizadas

- **Python 3.13+** — linguagem principal
- **FastAPI** — desenvolvimento da API REST
- **Uvicorn** — servidor da aplicação
- **SQLModel** — ORM e modelagem das tabelas
- **PostgreSQL** — banco de dados
- **Pydantic** — validação e schemas
- **Pydantic Settings** — gerenciamento das configurações
- **PyJWT** — autenticação utilizando JWT
- **Argon2** — hash e verificação de senhas
- **Requests** — comunicação com APIs externas
- **Pytest** — testes automatizados
- **validate-docbr** — validação de CPF

## Estrutura do projeto

```text
WorldCupBet/
│
├── src/
│   ├── config/
│   │
│   ├── controllers/
│   │
│   ├── enums/
│   │
│   ├── exceptions/
│   │
│   ├── models/
│   │
│   ├── repository/
│   │
│   ├── schemas/
│   │
│   ├── services/
│   │
│   └── database.py
│
├── testes/
│
├── .env
├── .gitignore
├── main.py
├── pytest.ini
├── requirements.txt
└── README.md
```

### Organização

O projeto utiliza uma separação entre as principais responsabilidades:

- **Controllers:** definem as rotas da API e recebem as requisições HTTP.
- **Services:** concentram as regras de negócio da aplicação.
- **Repositories:** responsáveis pelo acesso e pelas consultas ao banco de dados.
- **Models:** representam as entidades e tabelas do banco de dados.
- **Schemas:** responsáveis pela validação e estrutura dos dados de entrada e saída da API.
- **Config:** contém configurações da aplicação e mecanismos relacionados à autenticação.
- **Enums:** contém os valores enumerados utilizados pelo sistema.
- **Exceptions:** contém as exceções utilizadas no tratamento de erros.
- **Testes:** contém os testes automatizados da aplicação.

## Requisitos

Para executar o projeto, é necessário ter instalado:

* Python 3.13 ou superior
* PostgreSQL
* Git

## Instalação

Clone o repositório:

```bash
git clone https://github.com/Skrilas/WorldCupBet.git
```

Entre na pasta do projeto:

```bash
cd WorldCupBet
```

Crie um ambiente virtual:

```bash
python -m venv .venv
```

Ative o ambiente virtual no Windows:

```bash
.venv\Scripts\activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

## Variáveis de ambiente

O projeto utiliza um arquivo .env para armazenar configurações de banco de dados, autenticação e acesso às APIs externas.

Crie um arquivo `.env` na raiz do projeto:

```env
DATABASE_URL=
API_URL=
API_TOKEN=

HISTORICO_API_URL=
HISTORICO_API_KEY=

SECRET_KEY=

TEST_DATABASE_URL=
```

### Descrição das variáveis

| Variável | Descrição |
|---|---|
| `DATABASE_URL` | URL de conexão com o banco de dados principal. |
| `API_URL` | URL da API utilizada para obter dados das partidas. |
| `API_TOKEN` | Token de autenticação da API de partidas. |
| `HISTORICO_API_URL` | URL da API utilizada para obter dados históricos dos times. |
| `HISTORICO_API_KEY` | Chave de autenticação da API de dados históricos. |
| `SECRET_KEY` | Chave utilizada na geração e validação dos tokens JWT. |
| `TEST_DATABASE_URL` | URL de conexão com o banco de dados utilizado pelos testes automatizados. |

## Executando o projeto

Com o ambiente virtual ativado, execute:

```bash
uvicorn main:app --reload
```

Após iniciar o servidor, a API estará disponível localmente.

## Documentação da API

O projeto utiliza a documentação automática do FastAPI.

Após iniciar o servidor, acesse:

```text
http://127.0.0.1:8000/docs
```

A interface permite visualizar os endpoints, schemas, parâmetros e testar as requisições diretamente pelo navegador.

A autenticação utiliza JWT. Após realizar o login, o token de acesso pode ser utilizado para acessar as rotas protegidas.

## Testes

Os testes automatizados são executados utilizando Pytest.

Para executar:

```bash
pytest
```

Os testes utilizam um banco de dados separado do banco utilizado pela aplicação, evitando alterações nos dados reais durante a execução dos testes.

## Autenticação

A API utiliza autenticação baseada em JWT.

O fluxo básico é:

```text
Login
  ↓
Validação do usuário
  ↓
Geração do access token
  ↓
Requisição para rota protegida
  ↓
Validação do token
  ↓
Identificação do usuário
```

As rotas administrativas utilizam uma dependência adicional que verifica se o usuário autenticado possui permissão de administrador.

## Banco de dados

O projeto utiliza PostgreSQL para armazenamento dos dados.

Entre as principais entidades estão:

* Usuário
* Aposta
* Partida
* Time

As relações entre essas entidades são representadas através das chaves estrangeiras dos modelos SQLModel.

## APIs externas

O projeto utiliza duas APIs externas para obter dados relacionados à Copa do Mundo.

### Football-Data.org

Utilizada para obter informações sobre a competição e as partidas da Copa do Mundo.

- Site: https://www.football-data.org/
- URL: configurada através de `API_URL`
- Autenticação: `API_TOKEN`

### Zafronix FIFA World Cup API

Utilizada para obter informações históricas das seleções em Copas do Mundo.

- Site: https://api.zafronix.com/
- URL: configurada através de `HISTORICO_API_URL`
- Autenticação: `HISTORICO_API_KEY`
