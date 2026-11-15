# LogMind

## Regras inegociáveis

O dono do projeto revisa cada alteração. Por isso:

1. **Nunca faça commit.** Também não faça push, amend, merge, rebase nem qualquer operação que registre ou publique histórico. Deixe tudo no working tree. O máximo permitido é **sugerir uma mensagem de commit** no final do trabalho.
2. **Não adicione comentários no código.** Nenhum comentário, docstring, `TODO` ou explicação em linha, em qualquer linguagem (Python, TypeScript, Vue, CSS, HTML, YAML). Explicações vão na resposta do chat, não no código. Não remova comentários que já existem, a menos que seja pedido.
3. **Mantenha o diff pequeno e focado.** Altere só o que foi pedido. Não refatore, não renomeie e não reformate arquivos que você não precisa tocar, para que a revisão seja simples.
4. **Não troque de branch nem mexa no stage** (`git add`, `git restore --staged`) sem pedido explícito.

Mensagem de commit sugerida: Conventional Commits em português, no formato `tipo(escopo): resumo`, por exemplo `feat(front_end): adiciona tela de cadastro`. Tipos: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`.

## Sobre o projeto

Plataforma de análise de logs com I.A. O usuário envia arquivos `.log`, que são armazenados e registrados para posterior análise (contagem de linhas, erros, warnings e resumo gerado por I.A.).

- **Back-end:** Python 3.12, FastAPI, SQLAlchemy 2, Alembic, Pydantic Settings, PyJWT, argon2-cffi, PostgreSQL 16.
- **Front-end:** Vue 3, TypeScript, Vite, Pinia, Vue Router, Axios.
- **Infra:** Docker, Docker Compose, GitHub Actions (roda o `pytest` do back-end em PRs para a `main`).

Estado atual:

- Funcionam: cadastro (`POST /users`), login com JWT (`POST /users/login`), renovação de token (`POST /users/token/refresh`) e upload de `.log` (`POST /log_files/upload`, máximo de 5 MB, exige token).
- Os domínios `analysis` e `analysis_error` já têm model, schema, repository e service, mas ainda não estão expostos na API.
- Não existem endpoints de chat nem de I.A. O chat do front-end guarda o histórico no `localStorage` (por usuário) e as respostas são provisórias, até o back-end ganhar esses recursos.

## Estrutura e responsabilidades

### Raiz

- `docker-compose.yml`: sobe o PostgreSQL e a API.
- `.env.example`: modelo das variáveis do back-end e do Compose (banco, `SECRET_KEY`, `API_URL`, `DEBUG_MODE`). O `.env` real fica na raiz e não é versionado.
- `.github/workflows/tests.yml`: CI que instala `requirements-dev.txt` e roda o `pytest`.

### `back_end/`

Organizado por domínio, em camadas: **router → service → repository → model**.

- `app/main.py`: cria o app FastAPI, configura o CORS e registra os routers (`/users`, `/log_files`).
- `app/core/config.py`: `Settings` (Pydantic Settings), lê o `.env` da raiz do projeto.
- `app/core/security.py`: hash de senha (Argon2) e criação/validação dos JWT.
- `app/database/`: `base.py` (`Base` do SQLAlchemy), `connection.py` (engine), `session.py` (`SessionLocal`), `test_connection.py` (script manual para testar a conexão).
- `app/domains/<dominio>/`:
  - `model.py`: tabela do SQLAlchemy.
  - `schema.py`: modelos Pydantic de entrada e saída.
  - `repository.py`: acesso ao banco.
  - `service.py`: regras de negócio e tradução de erros para `HTTPException`.
  - `router.py`: rotas HTTP, sem regra de negócio.
  - `users/dependencies.py`: dependência `get_current_user`, que valida o Bearer token.
- `app/infrastructure/storage/`: `storage_interface.py` (contrato), `local_storage.py` e `s3_storage.py` (implementações).
- `alembic/`: migrations. O `env.py` carrega o `.env` da raiz e importa `app.domains` para registrar os models.
- `tests/unit/` e `tests/integration/`: testes com `pytest`. O `conftest.py` troca o engine por um SQLite temporário antes de importar `app.database.session`.
- `requirements.txt`: dependências para rodar a API (usado pelo `Dockerfile`). `requirements-dev.txt`: inclui o anterior e adiciona as de teste.
- `comandos.md`: comandos úteis do dia a dia.

### `front_end/`

- `src/main.ts`: inicializa o app (Pinia, Router e `styles/main.css`).
- `src/App.vue`: só renderiza o `RouterView`.
- `src/router/index.ts`: rotas e guards (`requiresAuth` para quem precisa estar logado, `guestOnly` para login e cadastro). Chat em `/chat/:chatId?`.
- `src/views/`: telas. `LoginView`, `RegisterView`, `ChatView`.
- `src/components/`:
  - `AuthLayout`: layout das telas de login e cadastro.
  - `BrandMark`: logo do LogMind em SVG.
  - `BaseButton`, `BaseInput`, `BasePasswordInput`: componentes de formulário reutilizáveis.
  - `ChatSidebar`: lista de chats agrupada por data, com botão de novo chat e logout.
  - `ChatMessageItem`: uma mensagem do chat.
  - `PromptInput`: campo de prompt.
- `src/stores/`: `auth.ts` (tokens, usuário lido do JWT, login, cadastro, logout) e `chat.ts` (chats, envio de prompt).
- `src/services/`:
  - `httpClient.ts`: instância do Axios com Bearer token e renovação automática ao receber 401.
  - `authService.ts`: chamadas de cadastro e login.
  - `chatService.ts`: persistência no `localStorage` e resposta provisória. Deve ser trocado por chamadas à API quando existirem os endpoints.
  - `tokenStorage.ts`: leitura e escrita dos tokens no `localStorage`.
- `src/types/`: interfaces TypeScript. `src/utils/`: `jwt.ts` (decodifica o payload) e `errors.ts` (extrai mensagem de erro da API).
- `src/styles/main.css`: tokens de design (cores, raios, fontes) com tema claro e escuro.
- `public/favicon.svg`: favicon.
- `.env.example`: `VITE_API_BASE_URL`. O Vite só lê o `.env` desta pasta e expõe ao navegador apenas variáveis `VITE_*`; nunca coloque segredos aqui.

## Indentação e estilo

- **Indentação com tabs, largura 4.** Vale para todo código novo (Python, TypeScript, Vue, CSS). É a configuração do editor do dono do projeto.
- Ao editar um arquivo que já usa espaços (no back-end isso acontece em `schema.py`, `router.py` de users, `config.py`, `tests/` e migrations), mantenha o estilo daquele arquivo e não reindente o arquivo inteiro.
- **Front-end:** o código TypeScript/JavaScript termina cada instrução com ponto e vírgula (`;`), e usa aspas simples. Arquivos `.vue` são formatados com o formatador da extensão Vue (Official). Estilos em `<style scoped>` e cores sempre por variáveis CSS de `main.css`, nunca valores fixos.
- **Python:** nomes em inglês e `snake_case` para funções e variáveis.
- **Idioma:** identificadores de código em inglês. Textos para o usuário (telas, mensagens de erro da API) em português do Brasil.

## Comandos

Back-end (a partir de `back_end/`, com o venv ativo):

```bash
pip install -r requirements-dev.txt
alembic upgrade head
uvicorn app.main:app --reload --port 5000
pytest
```

Front-end (a partir de `front_end/`):

```bash
npm install
npm run dev
npm run build
```

Tudo com Docker (a partir da raiz): `docker compose up --build`. A API sobe em `http://localhost:5000` e a documentação em `/docs`.

## Cuidados

- `app/database/session.py` executa `Base.metadata.create_all` ao ser importado. Por isso o `conftest.py` troca o engine antes de importar qualquer coisa de `app`; não mude essa ordem.
- Novas libs do back-end: edite `requirements.txt` (necessárias para rodar a API) ou `requirements-dev.txt` (só desenvolvimento e testes) à mão, com versão fixa. Não use `pip freeze`.
- Mudanças em models exigem uma migration (`alembic revision --autogenerate -m "mensagem"`), que o dono do projeto revisa antes de aplicar. Não rode `alembic upgrade` em bancos sem ele pedir.
- A porta da API é 5000 no Docker e no README, mas o `launch.json` do VS Code e o `__main__` do `main.py` usam 8000. O front aponta para `VITE_API_BASE_URL` (5000 por padrão).
- O CORS libera só `http://localhost:3000` e `http://localhost:5173`.
