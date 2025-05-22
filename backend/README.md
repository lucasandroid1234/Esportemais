# 🏀 Esporte+

Sistema web para agendamento e gerenciamento de horários em quadras esportivas públicas do município de Rio Verde – GO.

## 📋 Descrição
O projeto **Esporte+** tem como objetivo facilitar o acesso da população às quadras esportivas públicas, permitindo que usuários realizem agendamentos de forma simples e eficiente.

## 🚀 Tecnologias Utilizadas
- **Python 3.10**
- **FastAPI** – Framework web moderno e de alto desempenho
- **SQLAlchemy** – ORM para interação com o banco de dados
- **PostgreSQL** – Banco de dados relacional
- **Docker & Docker Compose** – Contêinerização e orquestração de serviços
- **Uvicorn** – Servidor ASGI para execução da aplicação
- **Pydantic** – Validação de dados
- **JWT** (via python-jose) – Autenticação baseada em tokens
- **Passlib** – Hashing de senhas

## 🧱 Estrutura do Projeto
O projeto está organizado em camadas para promover a separação de responsabilidades:

```bash
Esporte-/
├── auth/           # Gerenciamento de autenticação e autorização
├── database/       # Configuração e conexão com o banco de dados
├── models/         # Definição das entidades e seus relacionamentos
├── repository/     # Interação direta com o banco de dados
├── routers/        # Definição das rotas da API
├── schemas/        # Validação e serialização de dados com Pydantic
├── services/       # Regras de negócio da aplicação
├── main.py         # Ponto de entrada da aplicação
├── Dockerfile      # Configuração do Docker
└── docker-compose.yml # Orquestração dos containers
```

## ⚙️ Como Executar o Projeto

### Pré-requisitos
- Docker e Docker Compose instalados

### Passos
1. Clone o repositório:
    ```bash
    git clone https://github.com/RoggerMartins22/Esporte-.git
    cd Esporte-
    ```

2. Inicie os serviços com Docker Compose:
    ```bash
    docker-compose up --build
    ```

3. Acesse a aplicação:
   - Documentação Swagger: [http://localhost:8000/docs](http://localhost:8000/docs)
   - Documentação Redoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## 📡 Principais Rotas da API

### 👤 **Usuários**
- `POST /usuarios/cadastrar` – Cadastrar novo usuário.
- `POST /usuarios/login/` – Autenticar e receber um token JWT.
- `POST /usuarios/redefinir-senha/` – Redefine a senha do usuário.

### 🏟️ **Quadras**
- `POST /quadras/cadastrar` – Cadastrar nova quadra. (**ADM**)
- `GET /quadras/listar-quadras` – Listar quadras disponíveis
- `GET /quadras/listar-quadras/{id_quadra}` – Consulta Quadra
- `GET /quadras/horarios-disponiveis` – Listar horários disponíveis.
- `PUT /quadras/{id}` – Atualizar informações da quadra. (**ADM**)

### 📅 **Agendamentos**
- `POST /agendamentos/agendar-quadra` – Criar novo agendamento
- `GET /agendamentos/` – Listar agendamentos.
- `GET /agendamentos/quadra/{id_quadra}` – Listar agendamentos por Quadra.
- `GET /agendamentos/usuario/{id_usuario}` – Listar agendamentos por Usuário (**ADM**)
- `PUT /agendamentos/cancelar/{id_agendamento}` – Cancela um agendamento (usuário ou **ADM**)

⚠️ Algumas rotas são restritas a usuários com permissão de administrador (**ADM**).
