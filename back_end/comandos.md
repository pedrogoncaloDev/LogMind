### Gerar versão do banco
```
alembic revision --autogenerate -m "initial migration"
```

### Aplicar uma migration
```
alembic upgrade head
```