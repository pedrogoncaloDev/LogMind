FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd -m appuser
USER appuser 

# Em desenvolvimento: se DEBUG_MODE=true, sobe com debugpy escutando na porta 5678
# para o VS Code conectar (attach) e permitir breakpoints dentro do container.
CMD ["sh", "-c", "if [ \"$DEBUG_MODE\" = \"true\" ]; then python -m debugpy --listen 0.0.0.0:5678 --wait-for-client -m uvicorn app.main:app --host 0.0.0.0 --port 5000; else uvicorn app.main:app --host 0.0.0.0 --port 5000 --reload; fi"]

# Em produção
# CMD ["gunicorn", "main:app", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:5000"]