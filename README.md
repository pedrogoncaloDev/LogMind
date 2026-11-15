# LogMind

Plataforma de análise de logs com IA. O usuário envia arquivos `.log`, que são armazenados e registrados para posterior análise (contagem de linhas, erros, warnings e resumo gerado por IA).

> **Status:** em desenvolvimento. Autenticação e upload de logs estão funcionais; a análise com IA ainda está em construção (modelos e camadas de `analysis` / `analysis_error` já existem, mas ainda não estão expostos na API). O chat do front-end ainda não conversa com a API: o histórico fica no navegador e as respostas são provisórias.

## Funcionalidades

- Cadastro de usuários com senha protegida por **Argon2**
- Login com **JWT** (access token de 15 min + refresh token de 7 dias) e renovação de token
- Upload de arquivos `.log` (máx. 5 MB) por usuário autenticado
- Armazenamento de arquivos via interface plugável (local e S3)
- Migrations de banco com **Alembic**
- Testes unitários e de integração com **pytest**, executados no CI a cada Pull Request
- Front-end em Vue 3 com telas de login e cadastro, rotas protegidas e renovação automática do token
- Interface de chat: prompt e respostas na área principal e lista de chats agrupada por data na lateral. O histórico fica no `localStorage` e as respostas são provisórias, até a API ganhar endpoints de chat/IA
- Botão de anexo no campo de prompt para enviar arquivos `.log` (ainda sem funcionalidade)
- Tema claro e escuro, de acordo com o sistema

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
│   ├── requirements.txt       # dependências para rodar a API
│   ├── requirements-dev.txt   # as anteriores + dependências de teste
│   └── Dockerfile
├── front_end/                 # SPA Vue 3 + Vite
│   ├── public/                # favicon
│   └── src/
│       ├── components/        # AuthLayout, BrandMark, ChatSidebar, PromptInput, Base*
│       ├── router/            # rotas e guards de autenticação
│       ├── services/          # httpClient (Axios), authService, chatService, tokenStorage
│       ├── stores/            # Pinia: auth e chat
│       ├── styles/            # tokens de design (tema claro e escuro)
│       ├── types/ e utils/    # interfaces TypeScript e funções auxiliares
│       └── views/             # LoginView, RegisterView, ChatView
├── docker-compose.yml
├── .env.example
├── CLAUDE.md                  # instruções para o Claude Code
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

O front-end tem o próprio `.env` (veja [Front-end](#front-end)). O Vite só lê o `.env` da pasta `front_end/` e só expõe ao navegador variáveis `VITE_*`, por isso ele não usa o `.env` da raiz.

## Executando com Docker

```bash
docker compose up --build
```

Isso sobe o PostgreSQL e a API:

- API: http://localhost:5000
- Documentação interativa (Swagger): http://localhost:5000/docs
- Debug remoto (se `DEBUG_MODE=true`): porta `5678`

O Compose sobe apenas o banco e a API. O front-end roda à parte (veja [Front-end](#front-end)).

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

O `requirements-dev.txt` inclui o `requirements.txt` e adiciona as dependências de teste. Para apenas rodar a API, `pip install -r requirements.txt` basta.

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
npm run build          # checagem de tipos e build de produção
```

Acesse http://localhost:5173. A API precisa estar no ar no endereço definido em `VITE_API_BASE_URL` (padrão `http://localhost:5000`) para o login e o cadastro funcionarem.

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
- [ ] Upload de arquivos `.log` pelo front-end (o botão de anexo já existe, falta a funcionalidade)
- [ ] Listagem e detalhes dos logs enviados no front-end
- [ ] Endpoints de chat no back-end (hoje os chats vivem só no navegador)
- [ ] Dashboard
