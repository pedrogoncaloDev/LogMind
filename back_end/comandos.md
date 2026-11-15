### Gerar versão do banco
```
alembic revision --autogenerate -m "message"
```

### Aplicar uma migration
```
alembic upgrade head
```

### Instalar as libs para desenvolver e rodar os testes
```
pip install -r requirements-dev.txt
```

### Instalar só as libs necessárias para rodar a API (produção)
```
pip install -r requirements.txt
```

### Adicionar uma nova lib
Edite o arquivo à mão, fixando a versão (ex.: `nome-da-lib==1.2.3`):
- `requirements.txt`: libs que a API precisa para rodar.
- `requirements-dev.txt`: libs usadas só em desenvolvimento e testes (ex.: `pytest`).

Não use `pip freeze > requirements.txt`: ele despeja tudo o que está instalado no venv, inclusive as libs de teste, e mistura os dois arquivos.