# LogMind

Plataforma de análise de logs com IA. O usuário envia arquivos `.log`, que são armazenados e registrados para posterior análise (contagem de linhas, erros, warnings e resumo gerado por IA).

> **Status:** em desenvolvimento. Autenticação e upload de logs estão funcionais; a análise com IA ainda está em construção (modelos e camadas de `analysis` / `analysis_error` já existem, mas ainda não estão expostos na API).

## Funcionalidades

- Cadastro de usuários com senha protegida por **Argon2**
- Login com **JWT** (access token de 15 min + refresh token de 7 dias) e renovação de token
- Upload de arquivos `.log` (máx. 5 MB) por usuário autenticado
- Armazenamento de arquivos via interface plugável (local e S3)
- Migrations de banco com **Alembic**
- Testes unitários e de integração com **pytest**, executados no CI a cada Pull Request
- Frontend em Vue 3 com tela de login

## Stack

| Camada | Tecnologias |
| --- | --- |
| Back-end | Python 3.12, FastAPI, SQLAlchemy 2, Alembic, Pydantic Settings, PyJWT, argon2-cffi |
| Banco de dados | PostgreSQL 16 |
| Front-end | Vue 3, TypeScript, Vite, Pinia, Vue Router, PrimeVue, Axios |
| Infra | Docker, Docker Compose, GitHub Actions |

## Estrutura do projeto

```
LogMind/
├── back_end/
│   ├── app/
│   │   ├── core/              # configurações e segurança (hash, JWT)
│   │   ├── database/          # conexão, sessão e base do SQLAlchemy
│   │   ├── domains/           # users, log_files, analysis, analysis_error
│   │   │   └── <dominio>/     # model, schema, repository, service, router
│   │   ├── infrastructure/
│   │   │   └── storage/       # storage_interface, local_storage, s3_storage
│   │   └── main.py
│   ├── alembic/               # migrations
│   ├── tests/                 # unit/ e integration/
│   └── Dockerfile
├── front_end/                 # SPA Vue 3 + Vite
├── docker-compose.yml
├── .env.example
└── .github/workflows/tests.yml
```

O back-end segue uma organização por domínio, com separação em camadas (router → service → repository → model).

## Pré-requisitos

- Docker e Docker Compose **ou**
- Python 3.12+, Node.js 20+ e uma instância PostgreSQL

## Configuração

1. Copie o arquivo de variáveis de ambiente na raiz do projeto:

   ```bash
   cp .env.example .env
   ```

2. Ajuste os valores:

   | Variável | Descrição |
   | --- | --- |
   | `DB_HOST` | Host do PostgreSQL (`localhost` fora do Docker) |
   | `DB_PORT` | Porta do PostgreSQL |
   | `DB_NAME` / `DB_USER` / `DB_PASSWORD` | Credenciais do banco |
   | `API_URL` | URL da API (ex.: `http://localhost:5000`) |
   | `SECRET_KEY` | Chave usada para assinar os JWTs |
   | `DEBUG_MODE` | `true` sobe a API com `debugpy` na porta 5678 |
   | `STORAGE_LOCAL_PATH` | (opcional) pasta dos uploads, padrão `storage/uploads` |

## Executando com Docker

```bash
docker compose up --build
```

Isso sobe o PostgreSQL e a API:

- API: http://localhost:5000
- Documentação interativa (Swagger): http://localhost:5000/docs
- Debug remoto (se `DEBUG_MODE=true`): porta `5678`

Aplique as migrations (dentro do container ou localmente):

```bash
docker compose exec back_end alembic upgrade head
```

## Executando localmente

### Back-end

```bash
cd back_end
python -m venv venv
venv\Scripts\activate          # Windows  (Linux/macOS: source venv/bin/activate)
pip install -r requirements-dev.txt
alembic upgrade head
uvicorn app.main:app --reload --port 5000
```

Comandos úteis de migration:

```bash
alembic revision --autogenerate -m "mensagem"   # gerar migration
alembic upgrade head                             # aplicar migrations
```

### Front-end

```bash
cd front_end
cp .env.example .env
npm install
npm run dev
```

Acesse http://localhost:5173.

## Endpoints da API

| Método | Rota | Auth | Descrição |
| --- | --- | --- | --- |
| GET | `/health` | Não | Health check |
| POST | `/users` | Não | Cria um novo usuário |
| POST | `/users/login` | Não | Autentica e retorna access/refresh token |
| POST | `/users/token/refresh` | Não | Renova o access token |
| POST | `/log_files/upload` | Bearer | Envia um arquivo `.log` (máx. 5 MB) |

## Testes

```bash
cd back_end
pytest
```

Os testes rodam automaticamente no GitHub Actions em todo Pull Request para a `main`.

## Roadmap

- [ ] Endpoints de análise (`analysis`) e de erros encontrados (`analysis_error`)
- [ ] Integração com IA para resumo e classificação dos logs
- [ ] Listagem e detalhes dos logs enviados no front-end
- [ ] Telas de cadastro e dashboard