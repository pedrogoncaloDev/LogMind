FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd -m appuser
USER appuser 

# Em desenvolvimento
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000"]

# Em produção
# CMD ["gunicorn", "main:app", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:5000"]