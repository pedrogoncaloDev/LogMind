### Gerar versão do banco
```
alembic revision --autogenerate -m "initial migration"
```

### Aplicar uma migration
```
alembic upgrade head
```

### Atualizar o arquivo requirements.txt com as libs instaladas no venv via pip install
```
pip freeze > requirements.txt
```

### Instalar as libs do requirements.txt
```
pip install -r requirements.txt
```